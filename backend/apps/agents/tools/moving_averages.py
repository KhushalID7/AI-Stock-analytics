# backend/apps/agents/tools/moving_averages.py
from typing import Dict, Any
import io

import pandas as pd
from langchain.tools import tool


@tool
def moving_averages(csv_data: str, windows: str = "5,20,50") -> Dict[str, Any]:
    """
    Compute simple moving averages for given comma-separated windows.

    Args:
        csv_data: CSV string with columns including 'date' and 'close'
        windows: comma-separated ints, e.g. "5,20,50"

    Returns:
        {
          "ma": {
            "5": [{"date":"2025-01-01","value":123.4}, ...],
            "20": [...]
          },
          "last_values": {"5": 123.4, "20": 120.5}
        }

    On error returns {"error": "message"}.
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data), parse_dates=["date"]).sort_values("date")
        if "close" not in df.columns:
            return {"error": "close column not found in CSV data"}

        # parse windows
        window_list = []
        for token in windows.split(","):
            token = token.strip()
            if token:
                try:
                    window_list.append(int(token))
                except ValueError:
                    # ignore invalid tokens
                    continue

        if not window_list:
            return {"error": "no valid windows provided"}

        result: Dict[str, Any] = {"ma": {}, "last_values": {}}

        for w in window_list:
            col_name = f"sma_{w}"
            df[col_name] = df["close"].rolling(window=w).mean()

            pairs = []
            for d, v in zip(df["date"], df[col_name]):
                pairs.append({"date": d.strftime("%Y-%m-%d"), "value": (None if pd.isna(v) else float(v))})

            result["ma"][str(w)] = pairs

            # last non-null value for this SMA window
            non_null = df[col_name].dropna()
            last_val = float(non_null.iat[-1]) if not non_null.empty else None
            result["last_values"][str(w)] = last_val

        return result

    except Exception as e:
        return {"error": f"moving_averages failed: {str(e)}"}
