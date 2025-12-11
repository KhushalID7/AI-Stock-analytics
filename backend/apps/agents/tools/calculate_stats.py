from typing import Literal, Dict, Any
import io

import pandas as pd
from langchain.tools import tool


@tool
def calculate_stats(
    csv_data: str,
    metric: Literal["open", "high", "low", "close", "volume"] = "close",
) -> Dict[str, Any]:
    """
    Calculate basic descriptive statistics for a given metric in stock price CSV data.

    Args:
        csv_data: CSV string output from fetch_stock_prices. Must include columns:
                  date, open, high, low, close, volume.
        metric:   Which column to analyze. One of: 'open', 'high', 'low', 'close', 'volume'.

    Returns:
        A dict with statistics like:
        {
            "metric": "close",
            "count": 30,
            "mean": 123.45,
            "std": 4.56,
            "min": 120.0,
            "max": 130.0,
            "start_date": "2025-01-01",
            "end_date": "2025-01-31"
        }

    Note:
        If an error occurs, the returned dict will contain an "error" key with a message.
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data), parse_dates=["date"])

        if metric not in df.columns:
            return {
                "error": f"Metric '{metric}' not found in data. "
                         f"Available columns: {list(df.columns)}"
            }

        series = df[metric]

        if series.empty:
            return {"error": "No data available to compute statistics."}

        stats = {
            "metric": metric,
            "count": int(series.count()),
            "mean": float(series.mean()),
            "std": float(series.std()) if series.count() > 1 else 0.0,
            "min": float(series.min()),
            "max": float(series.max()),
            "start_date": df["date"].min().strftime("%Y-%m-%d"),
            "end_date": df["date"].max().strftime("%Y-%m-%d"),
        }
        return stats

    except Exception as e:
        return {"error": f"Failed to calculate statistics: {str(e)}"}
