from trading_strategy.strategies.trend.ema_cross import EmaCrossStrategy
from trading_strategy.strategies.trend.ema_cross_price_filter import EmaCrossPriceFilterStrategy
from trading_strategy.strategies.trend.ema_cross_price_slope_filter import EmaCrossPriceSlopeFilterStrategy
from trading_strategy.strategies.trend.ema_cross_trend_filter import EmaCrossTrendFilterStrategy
from trading_strategy.strategies.trend.ema_price_trend import EmaPriceTrendStrategy
from trading_strategy.strategies.trend.ema_triple_pullback import EmaTriplePullbackStrategy
from trading_strategy.strategies.trend.ema_triple_pullback_fast_exit import EmaTriplePullbackFastExitStrategy
from trading_strategy.strategies.trend.ema_triple_pullback_fast_exit_spread_filter import (
    EmaTriplePullbackFastExitSpreadFilterStrategy,
)
from trading_strategy.strategies.trend.ema_triple_stack import EmaTripleStackStrategy
from trading_strategy.strategies.trend.sma_cross import SmaCrossStrategy
from trading_strategy.strategies.trend.sma_triple_pullback_fast_exit import SmaTriplePullbackFastExitStrategy

__all__ = [
    "EmaCrossStrategy",
    "EmaCrossPriceFilterStrategy",
    "EmaCrossPriceSlopeFilterStrategy",
    "EmaCrossTrendFilterStrategy",
    "EmaPriceTrendStrategy",
    "EmaTriplePullbackStrategy",
    "EmaTriplePullbackFastExitStrategy",
    "EmaTriplePullbackFastExitSpreadFilterStrategy",
    "EmaTripleStackStrategy",
    "SmaCrossStrategy",
    "SmaTriplePullbackFastExitStrategy",
]
