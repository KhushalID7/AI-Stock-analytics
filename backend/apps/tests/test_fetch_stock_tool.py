import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from apps.agents.tools.fetch_stock_prices import fetch_stock_prices


def main():
    # Test 1: No date filters
    print("=== Test 1: No date filters ===")
    result = fetch_stock_prices.invoke({
        "symbol": "AAPL",
        "output_size": "compact"
    })

    if result.startswith("ERROR"):
        print(result)
    else:
        lines = result.splitlines()
        print(f"Total lines: {len(lines)}")
        print("\n".join(lines[:5]))
    
    # Test 2: With date filters (matching the actual data range)
    print("\n=== Test 2: With date filters ===")
    result = fetch_stock_prices.invoke({
        "symbol": "AAPL",
        "start_date": "2025-07-21",
        "end_date": "2025-07-25",
        "output_size": "compact"
    })

    if result.startswith("ERROR"):
        print(result)
    else:
        lines = result.splitlines()
        print(f"Total lines: {len(lines)}")
        print("\n".join(lines[:5]))


if __name__ == "__main__":
    main()
