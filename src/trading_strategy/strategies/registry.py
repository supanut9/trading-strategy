from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.benchmark.buy_and_hold import BuyAndHoldStrategy
from trading_strategy.strategies.breakout.bollinger_squeeze_breakout import BollingerSqueezeBreakoutStrategy
from trading_strategy.strategies.breakout.bollinger_squeeze_breakout_trend_filter import (
    BollingerSqueezeBreakoutTrendFilterStrategy,
)
from trading_strategy.strategies.breakout.donchian_breakout import DonchianBreakoutStrategy
from trading_strategy.strategies.mean_reversion.bollinger_mean_reversion import BollingerMeanReversionStrategy
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion import RsiMeanReversionStrategy
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_confirmation import (
    RsiMeanReversionConfirmationStrategy,
)
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_crossdown_exit import (
    RsiMeanReversionCrossdownExitStrategy,
)
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_crossdown_cooldown import (
    RsiMeanReversionCrossdownCooldownStrategy,
)
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_ema_filter import (
    RsiMeanReversionEmaFilterStrategy,
)
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_ema_slope_filter import (
    RsiMeanReversionEmaSlopeFilterStrategy,
)
from trading_strategy.strategies.mean_reversion.rsi_mean_reversion_ema_stack_filter import (
    RsiMeanReversionEmaStackFilterStrategy,
)
from trading_strategy.strategies.multi_indicator.rsi_ema_atr_price_structure import (
    RsiEmaAtrPriceStructureStrategy,
)
from trading_strategy.strategies.multi_indicator.rsi_ema_atr_volatility_filter import (
    RsiEmaAtrVolatilityFilterStrategy,
)
from trading_strategy.strategies.multi_timeframe.ema_regime_rsi_entry import EmaRegimeRsiEntryStrategy
from trading_strategy.strategies.pattern.double_top_bottom_reversal import DoubleTopBottomReversalStrategy
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
from trading_strategy.strategies.trend.ema_triple_pullback_trailing_exit import (
    EmaTriplePullbackTrailingExitStrategy,
)
from trading_strategy.strategies.trend.ema_triple_stack import EmaTripleStackStrategy
from trading_strategy.strategies.trend.sma_cross import SmaCrossStrategy
from trading_strategy.strategies.trend.sma_triple_pullback_fast_exit import SmaTriplePullbackFastExitStrategy


@dataclass(frozen=True)
class StrategyDefinition:
    name: str
    family: str
    description: str
    builder: type[Strategy]


STRATEGY_REGISTRY: dict[str, StrategyDefinition] = {
    "buy_and_hold": StrategyDefinition(
        name="buy_and_hold",
        family="benchmark",
        description="Benchmark that enters once and stays long.",
        builder=BuyAndHoldStrategy,
    ),
    "bollinger_squeeze_breakout": StrategyDefinition(
        name="bollinger_squeeze_breakout",
        family="breakout",
        description="Long-only breakout that requires Bollinger bandwidth compression before a channel breakout.",
        builder=BollingerSqueezeBreakoutStrategy,
    ),
    "bollinger_squeeze_breakout_trend_filter": StrategyDefinition(
        name="bollinger_squeeze_breakout_trend_filter",
        family="breakout",
        description="Bollinger squeeze breakout gated by price above a rising trend EMA.",
        builder=BollingerSqueezeBreakoutTrendFilterStrategy,
    ),
    "bollinger_mean_reversion": StrategyDefinition(
        name="bollinger_mean_reversion",
        family="mean_reversion",
        description="Long-only Bollinger mean reversion that buys the lower band and exits at the middle band.",
        builder=BollingerMeanReversionStrategy,
    ),
    "double_top_bottom_reversal": StrategyDefinition(
        name="double_top_bottom_reversal",
        family="pattern",
        description="Long-only reversal strategy that enters on double-bottom neckline breakouts and exits on double-top breakdowns.",
        builder=DoubleTopBottomReversalStrategy,
    ),
    "sma_cross": StrategyDefinition(
        name="sma_cross",
        family="trend",
        description="Trend-following moving average crossover.",
        builder=SmaCrossStrategy,
    ),
    "ema_cross": StrategyDefinition(
        name="ema_cross",
        family="trend",
        description="Trend-following exponential moving average crossover.",
        builder=EmaCrossStrategy,
    ),
    "ema_cross_price_filter": StrategyDefinition(
        name="ema_cross_price_filter",
        family="trend",
        description="EMA crossover that only trades when price is above a slower filter EMA.",
        builder=EmaCrossPriceFilterStrategy,
    ),
    "ema_cross_price_slope_filter": StrategyDefinition(
        name="ema_cross_price_slope_filter",
        family="trend",
        description="EMA crossover that requires price above a filter EMA and a rising filter EMA slope.",
        builder=EmaCrossPriceSlopeFilterStrategy,
    ),
    "ema_cross_trend_filter": StrategyDefinition(
        name="ema_cross_trend_filter",
        family="trend",
        description="EMA crossover that only trades when a higher-level EMA trend filter is bullish.",
        builder=EmaCrossTrendFilterStrategy,
    ),
    "ema_price_trend": StrategyDefinition(
        name="ema_price_trend",
        family="trend",
        description="Long only when price is above EMA and the EMA slope is rising.",
        builder=EmaPriceTrendStrategy,
    ),
    "ema_triple_stack": StrategyDefinition(
        name="ema_triple_stack",
        family="trend",
        description="Long only when fast, middle, and slow EMAs are stacked bullishly.",
        builder=EmaTripleStackStrategy,
    ),
    "ema_triple_pullback": StrategyDefinition(
        name="ema_triple_pullback",
        family="trend",
        description="Triple-EMA bullish alignment with pullback entry near the middle EMA.",
        builder=EmaTriplePullbackStrategy,
    ),
    "ema_triple_pullback_fast_exit": StrategyDefinition(
        name="ema_triple_pullback_fast_exit",
        family="trend",
        description="Triple-EMA bullish pullback entry with earlier exit on loss of fast EMA support.",
        builder=EmaTriplePullbackFastExitStrategy,
    ),
    "ema_triple_pullback_fast_exit_spread_filter": StrategyDefinition(
        name="ema_triple_pullback_fast_exit_spread_filter",
        family="trend",
        description="Triple-EMA bullish pullback entry with early exit and minimum EMA spread requirements.",
        builder=EmaTriplePullbackFastExitSpreadFilterStrategy,
    ),
    "ema_triple_pullback_trailing_exit": StrategyDefinition(
        name="ema_triple_pullback_trailing_exit",
        family="trend",
        description="Triple-EMA bullish pullback entry with exit on loss of a configurable trailing EMA.",
        builder=EmaTriplePullbackTrailingExitStrategy,
    ),
    "rsi_mean_reversion": StrategyDefinition(
        name="rsi_mean_reversion",
        family="mean_reversion",
        description="Long-only RSI mean reversion entry and exit.",
        builder=RsiMeanReversionStrategy,
    ),
    "rsi_mean_reversion_confirmation": StrategyDefinition(
        name="rsi_mean_reversion_confirmation",
        family="mean_reversion",
        description="Long-only RSI mean reversion that waits for RSI to recover back above oversold before entering.",
        builder=RsiMeanReversionConfirmationStrategy,
    ),
    "rsi_mean_reversion_crossdown_exit": StrategyDefinition(
        name="rsi_mean_reversion_crossdown_exit",
        family="mean_reversion",
        description="Long-only RSI mean reversion that exits when RSI crosses back down below overbought.",
        builder=RsiMeanReversionCrossdownExitStrategy,
    ),
    "rsi_mean_reversion_crossdown_cooldown": StrategyDefinition(
        name="rsi_mean_reversion_crossdown_cooldown",
        family="mean_reversion",
        description="Long-only RSI mean reversion with cross-down exit and a cooldown after each exit.",
        builder=RsiMeanReversionCrossdownCooldownStrategy,
    ),
    "rsi_mean_reversion_ema_filter": StrategyDefinition(
        name="rsi_mean_reversion_ema_filter",
        family="mean_reversion",
        description="Long-only RSI mean reversion that only trades above a filter EMA.",
        builder=RsiMeanReversionEmaFilterStrategy,
    ),
    "rsi_mean_reversion_ema_slope_filter": StrategyDefinition(
        name="rsi_mean_reversion_ema_slope_filter",
        family="mean_reversion",
        description="Long-only RSI mean reversion that only trades when a filter EMA is rising.",
        builder=RsiMeanReversionEmaSlopeFilterStrategy,
    ),
    "rsi_mean_reversion_ema_stack_filter": StrategyDefinition(
        name="rsi_mean_reversion_ema_stack_filter",
        family="mean_reversion",
        description="Long-only RSI mean reversion that only trades when a fast EMA is above a slow EMA.",
        builder=RsiMeanReversionEmaStackFilterStrategy,
    ),
    "rsi_ema_atr_price_structure": StrategyDefinition(
        name="rsi_ema_atr_price_structure",
        family="multi_indicator",
        description="RSI entry and cross-down exit with EMA regime, ATR volatility gate, and recent price-structure filter.",
        builder=RsiEmaAtrPriceStructureStrategy,
    ),
    "rsi_ema_atr_volatility_filter": StrategyDefinition(
        name="rsi_ema_atr_volatility_filter",
        family="multi_indicator",
        description="RSI entry and cross-down exit with EMA regime and ATR volatility filter.",
        builder=RsiEmaAtrVolatilityFilterStrategy,
    ),
    "ema_regime_rsi_entry": StrategyDefinition(
        name="ema_regime_rsi_entry",
        family="multi_timeframe",
        description="1h RSI mean-reversion entry and cross-down exit gated by a completed 4h EMA regime filter.",
        builder=EmaRegimeRsiEntryStrategy,
    ),
    "donchian_breakout": StrategyDefinition(
        name="donchian_breakout",
        family="breakout",
        description="Long-only Donchian breakout with channel exit.",
        builder=DonchianBreakoutStrategy,
    ),
    "sma_triple_pullback_fast_exit": StrategyDefinition(
        name="sma_triple_pullback_fast_exit",
        family="trend",
        description="Triple-SMA bullish pullback entry with earlier exit on loss of fast SMA support.",
        builder=SmaTriplePullbackFastExitStrategy,
    ),
}


def available_strategies() -> list[StrategyDefinition]:
    return sorted(STRATEGY_REGISTRY.values(), key=lambda definition: (definition.family, definition.name))


def build_strategy(name: str, params: dict | None = None) -> Strategy:
    definition = STRATEGY_REGISTRY.get(name)
    if definition is None:
        raise ValueError(f"Unknown strategy: {name}")
    return definition.builder(**(params or {}))


def expand_strategy_grid(strategy_specs: list[dict]) -> list[Strategy]:
    strategies: list[Strategy] = []
    for strategy_spec in strategy_specs:
        name = strategy_spec["name"]
        parameter_grid = strategy_spec.get("params", {})
        normalized_items = {
            key: value if isinstance(value, list) else [value]
            for key, value in parameter_grid.items()
        }

        if not normalized_items:
            strategies.append(build_strategy(name))
            continue

        keys = list(normalized_items.keys())
        value_sets = [normalized_items[key] for key in keys]
        for combination in product(*value_sets):
            params = dict(zip(keys, combination, strict=True))
            strategies.append(build_strategy(name, params))

    return strategies
