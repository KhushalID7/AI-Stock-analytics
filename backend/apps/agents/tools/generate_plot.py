from typing import Literal
import io
import uuid
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from langchain.tools import tool


# Base folder: apps/static/charts (relative to this file)
BASE_DIR = Path(__file__).resolve().parents[2]  # .../backend/apps
CHARTS_DIR = BASE_DIR / "static" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


@tool
def generate_plot(
    csv_data: str,
    x: str = "date",
    y: str = "close",
    chart_type: Literal["line"] = "line",
) -> str:
    """
    Generate a chart from stock price CSV data and return a URL to the saved image.

    Args:
        csv_data: CSV string output from fetch_stock_prices. Should include a 'date' column.
        x:        Column name for the x-axis (typically 'date').
        y:        Column name for the y-axis (e.g. 'close', 'open', 'volume').
        chart_type: For now only 'line' is supported, but this can be extended later.

    Returns:
        A URL path like '/static/charts/<filename>.png' that the frontend can render directly.

    If an error occurs, the function returns a string starting with "ERROR:" describing the problem.
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data), parse_dates=[x])

        if x not in df.columns:
            return (f"ERROR: x-axis column '{x}' not found in data. "
                    f"Available columns: {list(df.columns)}")
        if y not in df.columns:
            return (f"ERROR: y-axis column '{y}' not found in data. "
                    f"Available columns: {list(df.columns)}")

        if df.empty:
            return "ERROR: No data available to plot."

        # Sort by x for nicer plotting
        df = df.sort_values(by=x)

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 4))
        if chart_type == "line":
            ax.plot(df[x], df[y])
        else:
            ax.plot(df[x], df[y])

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} over time")
        fig.autofmt_xdate()
        plt.tight_layout()

        # Save to a unique file
        filename = f"chart_{uuid.uuid4().hex}.png"
        filepath = CHARTS_DIR / filename
        fig.savefig(filepath)
        plt.close(fig)

        # URL that FastAPI will serve (we'll mount /static)
        url_path = f"/static/charts/{filename}"
        return url_path

    except Exception as e:
        return f"ERROR: Failed to generate plot: {str(e)}"
