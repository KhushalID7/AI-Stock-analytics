import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from apps.services.alpha_vantage_client import AlphaVantageClient

def main():
    client = AlphaVantageClient()
    df = client.fetch_daily("AAPL", output_size="compact")
    print(df.head())
    print(df.tail())

if __name__ == "__main__":
    main()
