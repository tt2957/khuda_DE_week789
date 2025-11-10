import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# 항상 프로젝트 루트 기준으로 경로 잡기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

# .env 파일에서 API 키 불러오기
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_data(region="KR", max_results=50):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": max_results,
        "key": API_KEY
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    df = pd.json_normalize(data["items"])
    os.makedirs("raw_data", exist_ok=True)
    filename = f"raw_data/youtube_trending_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

if __name__ == "__main__":
    try:
        fetch_youtube_data()
    except Exception as e:
        print(f"❌ Error: {e}")
