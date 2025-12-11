# backend/apps/agents/tools/bollinger.py
from typing import Dict, Any
import io

import pandas as pd
from langchain.tools import tool


@tool
def bollinger_bands(csv_data: str, window: int = 20, num_std: float = 2.0) -> Dict[str, Any]:
    """
    Compute Bollinger Bands (SMA, upper, lower) for the 'close' price.

    Args:
        csv_data: CSV string with 'date' and 'close'
        window: rolling window for SMA/std
        num_std: multiplier for bands (default 2.0)

    Returns:
        {
          "bands": [{"date":"2025-01-01","sma":..,"upper":..,"lower":..}, ...],
          "last": {"date": "...", "sma":.., "upper":.., "lower":..}
        }

    On error returns {"error": "message"}.
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data), parse_dates=["date"]).sort_values("date")
        if "close" not in df.columns:
            return {"error": "close column not found in CSV data"}

        df["sma"] = df["close"].rolling(window=window).mean()
        df["std"] = df["close"].rolling(window=window).std()
        df["upper"] = df["sma"] + (df["std"] * num_std)
        df["lower"] = df["sma"] - (df["std"] * num_std)

        rows = []
        for d, sma, up, lo in zip(df["date"], df["sma"], df["upper"], df["lower"]):
            rows.append({
                "date": d.strftime("%Y-%m-%d"),
                "sma": (None if pd.isna(sma) else float(sma)),
                "upper": (None if pd.isna(up) else float(up)),
                "lower": (None if pd.isna(lo) else float(lo)),
            })

        last = rows[-1] if rows else {}
        return {"bands": rows, "last": last}
    except Exception as e:
        return {"error": f"bollinger_bands failed: {str(e)}"}
