import os
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE")

BASE_URL = "https://www.alphavantage.co/query"

class AlphaVantageClient:
    def __init__(self,api_key: str = None):
        self.api_key = api_key or ALPHA_VANTAGE_API_KEY
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment variables.")
        
    def fetch_daily(self, symbol:str, output_size:str = "compact") -> pd.DataFrame:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": output_size,
            "apikey": self.api_key
        }

        response = requests.get(BASE_URL,params=params)
        data = response.json()
        if "Error Message" in data:
            raise ValueError(f"Invalid symbol or API error: {data['Error Message']}")

        if "Note" in data:
            raise RuntimeError(
                "API rate limit exceeded. Alpha Vantage free tier allows ~25 calls/day."
            )

        if "Time Series (Daily)" not in data:
            raise RuntimeError("Unexpected API response format.")
        

        ts = data["Time Series (Daily)"]

        df = pd.DataFrame.from_dict(ts,orient="index")

        df.index = pd.to_datetime(df.index)

        df.columns = ["open","high","low","close","volume"]

        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": int
        })

        # Sort by date
        df = df.sort_index()

        return df
