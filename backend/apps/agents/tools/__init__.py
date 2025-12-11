from .fetch_stock_prices import fetch_stock_prices
from .calculate_stats import calculate_stats
from .generate_plot import generate_plot
from .moving_averages import moving_averages
from .bollinger import bollinger_bands


# You will keep extending this list as you add more tools.
ALL_TOOLS = [
    fetch_stock_prices,
    calculate_stats,
    generate_plot,
    moving_averages,
    bollinger_bands
]
