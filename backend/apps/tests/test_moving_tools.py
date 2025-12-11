# backend/apps/tests/test_moving_tools.py
from apps.agents.tools.fetch_stock_prices import fetch_stock_prices
from apps.agents.tools.moving_averages import moving_averages
from apps.agents.tools.bollinger import bollinger_bands

def main():
    print("Fetching CSV for AAPL (compact)...")
    csv = fetch_stock_prices.invoke({"symbol": "AAPL", "output_size": "compact"})
    print("CSV length:", len(csv) if isinstance(csv, str) else "not a string")

    print("\nTesting moving_averages (windows=5,20):")
    ma = moving_averages.invoke({"csv_data": csv, "windows": "5,20"})
    print("moving_averages result keys:", list(ma.keys()))
    print("last_values:", ma.get("last_values"))

    print("\nTesting bollinger_bands (window=20):")
    bb = bollinger_bands.invoke({"csv_data": csv, "window": 20, "num_std": 2.0})
    print("bollinger_bands keys:", list(bb.keys()))
    print("last band:", bb.get("last"))

if __name__ == "__main__":
    main()
