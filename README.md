# social-sentiment-dashboard

📢 Real-Time Reddit Sentiment Dashboard
A Streamlit proof-of-concept that scrapes the latest Reddit posts for one or more stock tickers, runs VADER sentiment analysis, and displays an interactive live sentiment chart—no API keys required.

🔍 What it does
Enter comma-separated stock tickers (e.g., TSLA, NVDA).

Fetch the most recent Reddit posts for each ticker via Reddit’s public JSON search endpoint.

Score each post’s sentiment using NLTK’s VADER (compound polarity).

Visualize hourly average sentiment per ticker in a Plotly line chart.

Inspect the raw scored posts in a table.

Download the full scored dataset as CSV.

Demo only—unauthenticated scraping, no rate-limit backoff or enterprise streaming.
For production-grade sentiment pipelines (FinBERT models, Kafka streams), contact me.

✨ Key Features
Zero setup: no API keys, no credentials—uses public Reddit JSON.

CPU-friendly: VADER is lightweight and runs instantly on any machine.

Live refresh: simply click “Fetch sentiment” to update with the latest posts.

Interactive visuals: Plotly chart with zoom, hover tooltips, and legend filtering.

Downloadable data: export your scored posts as reddit_sentiment.csv.

🚀 Quick Start (Local)
bash
Copy
Edit
git clone https://github.com/THartyMBA/social-sentiment-dashboard.git
cd social-sentiment-dashboard
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run social_sentiment_dashboard.py
Open your browser to http://localhost:8501.

Enter one or more tickers and click Fetch sentiment.

☁️ Deploy on Streamlit Community Cloud
Push this repo to GitHub under THartyMBA (public or private).

Visit streamlit.io/cloud → New app → select your repo/branch.

Click Deploy—no secrets or tokens needed.

🛠️ Requirements
text
Copy
Edit
streamlit>=1.32
pandas
plotly
nltk
requests
The first run will download NLTK’s VADER lexicon automatically.

🗂️ Repo Structure
kotlin
Copy
Edit
social-sentiment-dashboard/
├─ social_sentiment_dashboard.py   ← single-file Streamlit app
├─ requirements.txt
└─ README.md                       ← this file
📜 License
CC0 1.0 – public-domain dedication. Attribution appreciated but not required.

🙏 Acknowledgements
Streamlit – rapid Python UIs

NLTK VADER – rule-based sentiment analysis

Plotly – interactive charting

Reddit’s public JSON API – free, no-key data access

Monitor live social sentiment in seconds—enjoy! 🎉
