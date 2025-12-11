from typing import Optional, Literal
from datetime import datetime
import pandas as pd

from langchain.tools import tool # type: ignore

from apps.services.alpha_vantage_client import AlphaVantageClient


def _parse_date(date_str: str):
    """Parse a YYYY-MM-DD string into a datetime object."""
    return pd.to_datetime(date_str)


@tool
def fetch_stock_prices(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    output_size: Literal["compact", "full"] = "compact",
) -> str:
    """
    Fetch daily OHLCV stock price data as a CSV string for a given symbol.

    Dates should be in 'YYYY-MM-DD' format.
    - symbol: Stock ticker symbol, e.g. 'AAPL', 'TSLA', 'INFY'.
    - start_date: Filter data from this date (inclusive). Optional.
    - end_date: Filter data up to this date (inclusive). Optional.
    - output_size: 'compact' for ~100 recent days, 'full' for full history.

    Returns:
        CSV string with columns: date, open, high, low, close, volume.

    If an error occurs (invalid symbol, API limit, etc.), returns a
    human-readable error message starting with 'ERROR:' so the LLM can
    decide what to do.
    """
    try:
        client = AlphaVantageClient()
        df = client.fetch_daily(symbol=symbol, output_size=output_size)

        # Apply date filters if provided
        if start_date:
            start = _parse_date(start_date)
            df = df[df.index >= start]

        if end_date:
            end = _parse_date(end_date)
            df = df[df.index <= end]

        if df.empty:
            return f"ERROR: No data available for {symbol} in the given date range."

        csv_str = df.to_csv(index=True, index_label="date")
        return csv_str

    except ValueError as ve:
        return f"ERROR: {str(ve)}"
    
    except RuntimeError as re:
        return f"ERROR: {str(re)}"
    
    except Exception as e:
        return f"ERROR: Unexpected error while fetching stock prices: {str(e)}"
