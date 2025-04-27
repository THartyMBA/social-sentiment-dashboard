# social_sentiment_dashboard.py
"""
Real-Time Reddit Sentiment Dashboard  📢📈
────────────────────────────────────────────────────────────────────────────
Enter one or more stock tickers.  
The app scrapes the 100 most-recent Reddit posts for each ticker
(no API key; uses Reddit’s public JSON endpoint), runs VADER sentiment,
and streams a live score chart that updates on refresh.

> Fast + free; perfect demo for NLP streaming work.  
> For production pipelines (auth, rate-limit back-off, FinBERT, Kafka),
  contact me → https://drtomharty.com/bio
"""
# ───────────────────────────────────────── imports ────────────────────────
import requests, time, datetime as dt
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk, os

# ensure VADER lexicon (downloaded once, cached)
nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

# ───────────────────────── scraping helper ───────────────────────────────
HEADERS = {"User-agent": "sentiment-dashboard-demo"}

def fetch_reddit_posts(query, limit=100):
    url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&size={limit}"
    res = requests.get(url, timeout=20)
    res.raise_for_status()
    data = res.json().get("data", [])
    posts = []
    for post in data:
        ts = post.get("created_utc")
        text = (post.get("title","") + " " + post.get("selftext","")).strip()
        if ts and text:
            posts.append((ts, text))
    return posts

def score_posts(posts):
    rows = []
    for ts, text in posts:
        score = sia.polarity_scores(text)["compound"]
        rows.append({"timestamp": dt.datetime.utcfromtimestamp(ts), "text": text, "compound": score})
    return pd.DataFrame(rows)

# ───────────────────────── UI  ───────────────────────────────────────────
st.set_page_config(page_title="Reddit Sentiment Dashboard", layout="wide")
st.title("📢 Real-Time Reddit Sentiment Dashboard")

st.info(
    "🔔 **Demo Notice**  \n"
    "Free, unauthenticated scrape of Reddit’s public JSON; suitable for demos. "
    "For enterprise-grade streaming NLP stacks, [contact me](https://drtomharty.com/bio).",
    icon="💡"
)

tickers = st.text_input("Enter comma-separated stock tickers (e.g., TSLA, NVDA, GME)",
                        value="TSLA").upper().replace(" ","").split(",")
limit = st.slider("Posts per ticker", 20, 100, 60, 10)

if st.button("🚀 Fetch sentiment"):
    all_dfs = []
    with st.spinner("Scraping & scoring…"):
        for tkr in tickers:
            posts = fetch_reddit_posts(tkr, limit=limit)
            if not posts:
                continue
            df = score_posts(posts)
            df["ticker"] = tkr
            all_dfs.append(df)

    if not all_dfs:
        st.warning("No posts found. Try different ticker or higher limit.")
        st.stop()

    data = pd.concat(all_dfs)

    # ─── Chart ─────────────────────────────────────────
    st.subheader("Average sentiment over time")
    # resample per hour for smoother line
    data.set_index("timestamp", inplace=True)
    hourly = data.groupby("ticker").resample("1H")["compound"].mean().reset_index()
    fig = px.line(hourly, x="timestamp", y="compound", color="ticker",
                  title="Hourly Avg VADER Compound Score (↑ positive, ↓ negative)",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # ─── Table & download ─────────────────────────────
    st.subheader("Raw scored posts")
    st.dataframe(data.reset_index())

    st.download_button("⬇️ Download scored data CSV",
                       data.reset_index().to_csv(index=False).encode(),
                       file_name="reddit_sentiment.csv",
                       mime="text/csv")
