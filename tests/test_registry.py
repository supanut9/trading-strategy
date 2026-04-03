import unittest

from trading_strategy.strategies import available_strategies, expand_strategy_grid


class StrategyRegistryTests(unittest.TestCase):
    def test_available_strategies_are_grouped_by_family(self) -> None:
        catalog = available_strategies()

        self.assertEqual(
            [definition.name for definition in catalog],
            [
                "buy_and_hold",
                "bollinger_squeeze_breakout",
                "bollinger_squeeze_breakout_trend_filter",
                "donchian_breakout",
                "bollinger_mean_reversion",
                "rsi_mean_reversion",
                "rsi_mean_reversion_confirmation",
                "rsi_mean_reversion_crossdown_cooldown",
                "rsi_mean_reversion_crossdown_exit",
                "rsi_mean_reversion_ema_filter",
                "rsi_mean_reversion_ema_slope_filter",
                "rsi_mean_reversion_ema_stack_filter",
                "rsi_ema_atr_price_structure",
                "rsi_ema_atr_volatility_filter",
                "double_top_bottom_reversal",
                "ema_cross",
                "ema_cross_price_filter",
                "ema_cross_price_slope_filter",
                "ema_cross_trend_filter",
                "ema_price_trend",
                "ema_triple_pullback",
                "ema_triple_pullback_fast_exit",
                "ema_triple_pullback_fast_exit_spread_filter",
                "ema_triple_pullback_trailing_exit",
                "ema_triple_stack",
                "sma_cross",
                "sma_triple_pullback_fast_exit",
            ],
        )

    def test_expand_strategy_grid_builds_all_parameter_combinations(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "sma_cross",
                    "params": {
                        "short_window": [12, 24],
                        "long_window": [72, 144],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(strategies[0].parameters, {"short_window": 12, "long_window": 72})
        self.assertEqual(strategies[-1].parameters, {"short_window": 24, "long_window": 144})

    def test_expand_strategy_grid_builds_bollinger_squeeze_breakout_parameters(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "bollinger_squeeze_breakout",
                    "params": {
                        "period": [20],
                        "band_width": [2.0],
                        "squeeze_threshold_pct": [4.0, 6.0],
                        "breakout_lookback": [20],
                        "exit_lookback": [10],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 20,
                "band_width": 2.0,
                "squeeze_threshold_pct": 4.0,
                "breakout_lookback": 20,
                "exit_lookback": 10,
            },
        )

    def test_expand_strategy_grid_builds_bollinger_squeeze_breakout_trend_filter_parameters(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "bollinger_squeeze_breakout_trend_filter",
                    "params": {
                        "period": [30],
                        "band_width": [2.0],
                        "squeeze_threshold_pct": [4.0],
                        "breakout_lookback": [55],
                        "exit_lookback": [20],
                        "trend_ema_window": [100, 150],
                        "trend_slope_window": [3],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 30,
                "band_width": 2.0,
                "squeeze_threshold_pct": 4.0,
                "breakout_lookback": 55,
                "exit_lookback": 20,
                "trend_ema_window": 100,
                "trend_slope_window": 3,
            },
        )

    def test_expand_strategy_grid_builds_ema_cross_parameters(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_cross",
                    "params": {
                        "short_window": [12],
                        "long_window": [48, 96],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(strategies[0].parameters, {"short_window": 12, "long_window": 48})
        self.assertEqual(strategies[1].parameters, {"short_window": 12, "long_window": 96})

    def test_expand_strategy_grid_builds_ema_variation_parameters(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_price_trend",
                    "params": {
                        "ema_window": [55],
                        "slope_window": [3, 6],
                    },
                },
                {
                    "name": "ema_triple_stack",
                    "params": {
                        "fast_window": [8],
                        "middle_window": [21],
                        "slow_window": [89, 144],
                    },
                },
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(strategies[0].parameters, {"ema_window": 55, "slope_window": 3})
        self.assertEqual(strategies[1].parameters, {"ema_window": 55, "slope_window": 6})
        self.assertEqual(
            strategies[2].parameters,
            {"fast_window": 8, "middle_window": 21, "slow_window": 89},
        )

    def test_expand_strategy_grid_builds_filtered_ema_variants(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_cross_price_filter",
                    "params": {
                        "short_window": [9],
                        "long_window": [21],
                        "filter_window": [200],
                    },
                },
                {
                    "name": "ema_cross_trend_filter",
                    "params": {
                        "short_window": [9],
                        "long_window": [21],
                        "trend_fast_window": [50],
                        "trend_slow_window": [200],
                    },
                },
                {
                    "name": "ema_triple_pullback",
                    "params": {
                        "fast_window": [9],
                        "middle_window": [21],
                        "slow_window": [55],
                        "pullback_pct": [0.003],
                    },
                },
            ]
        )

        self.assertEqual(len(strategies), 3)
        self.assertEqual(
            strategies[0].parameters,
            {"short_window": 9, "long_window": 21, "filter_window": 200},
        )
        self.assertEqual(
            strategies[1].parameters,
            {
                "short_window": 9,
                "long_window": 21,
                "trend_fast_window": 50,
                "trend_slow_window": 200,
            },
        )
        self.assertEqual(
            strategies[2].parameters,
            {"fast_window": 9, "middle_window": 21, "slow_window": 55, "pullback_pct": 0.003},
        )

    def test_expand_strategy_grid_builds_new_ema_refinements(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_cross_price_slope_filter",
                    "params": {
                        "short_window": [34],
                        "long_window": [55],
                        "filter_window": [200],
                        "slope_window": [3],
                    },
                },
                {
                    "name": "ema_triple_pullback_fast_exit",
                    "params": {
                        "fast_window": [9],
                        "middle_window": [21],
                        "slow_window": [55],
                        "pullback_pct": [0.003],
                    },
                },
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "short_window": 34,
                "long_window": 55,
                "filter_window": 200,
                "slope_window": 3,
            },
        )
        self.assertEqual(
            strategies[1].parameters,
            {"fast_window": 9, "middle_window": 21, "slow_window": 55, "pullback_pct": 0.003},
        )

    def test_expand_strategy_grid_builds_ema_spread_filter_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_triple_pullback_fast_exit_spread_filter",
                    "params": {
                        "fast_window": [12],
                        "middle_window": [20],
                        "slow_window": [43],
                        "pullback_pct": [0.00125],
                        "min_fast_middle_spread_pct": [0.001, 0.0015],
                        "min_middle_slow_spread_pct": [0.0015],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "fast_window": 12,
                "middle_window": 20,
                "slow_window": 43,
                "pullback_pct": 0.00125,
                "min_fast_middle_spread_pct": 0.001,
                "min_middle_slow_spread_pct": 0.0015,
            },
        )
        self.assertEqual(
            strategies[1].parameters,
            {
                "fast_window": 12,
                "middle_window": 20,
                "slow_window": 43,
                "pullback_pct": 0.00125,
                "min_fast_middle_spread_pct": 0.0015,
                "min_middle_slow_spread_pct": 0.0015,
            },
        )

    def test_expand_strategy_grid_builds_sma_pullback_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "sma_triple_pullback_fast_exit",
                    "params": {
                        "fast_window": [12],
                        "middle_window": [20],
                        "slow_window": [43, 45],
                        "pullback_pct": [0.00125],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {"fast_window": 12, "middle_window": 20, "slow_window": 43, "pullback_pct": 0.00125},
        )
        self.assertEqual(
            strategies[1].parameters,
            {"fast_window": 12, "middle_window": 20, "slow_window": 45, "pullback_pct": 0.00125},
        )

    def test_expand_strategy_grid_builds_rsi_ema_filter_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_ema_filter",
                    "params": {
                        "period": [22],
                        "oversold": [18, 21],
                        "overbought": [64],
                        "filter_window": [150, 200],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(
            strategies[0].parameters,
            {"period": 22, "oversold": 18, "overbought": 64, "filter_window": 150},
        )
        self.assertEqual(
            strategies[-1].parameters,
            {"period": 22, "oversold": 21, "overbought": 64, "filter_window": 200},
        )

    def test_expand_strategy_grid_builds_rsi_ema_slope_filter_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_ema_slope_filter",
                    "params": {
                        "period": [22],
                        "oversold": [21],
                        "overbought": [63],
                        "filter_window": [100, 150],
                        "slope_window": [3, 6],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 22,
                "oversold": 21,
                "overbought": 63,
                "filter_window": 100,
                "slope_window": 3,
            },
        )

    def test_expand_strategy_grid_builds_rsi_ema_stack_filter_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_ema_stack_filter",
                    "params": {
                        "period": [22],
                        "oversold": [21],
                        "overbought": [63],
                        "fast_filter_window": [21, 50],
                        "slow_filter_window": [100],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 22,
                "oversold": 21,
                "overbought": 63,
                "fast_filter_window": 21,
                "slow_filter_window": 100,
            },
        )

    def test_expand_strategy_grid_builds_rsi_confirmation_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_confirmation",
                    "params": {
                        "period": [22],
                        "oversold": [18, 21],
                        "overbought": [63, 64],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(
            strategies[0].parameters,
            {"period": 22, "oversold": 18, "overbought": 63},
        )
        self.assertEqual(
            strategies[-1].parameters,
            {"period": 22, "oversold": 21, "overbought": 64},
        )

    def test_expand_strategy_grid_builds_rsi_crossdown_exit_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_crossdown_exit",
                    "params": {
                        "period": [22],
                        "oversold": [18, 21],
                        "overbought": [63, 64],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 4)
        self.assertEqual(
            strategies[0].parameters,
            {"period": 22, "oversold": 18, "overbought": 63},
        )
        self.assertEqual(
            strategies[-1].parameters,
            {"period": 22, "oversold": 21, "overbought": 64},
        )

    def test_expand_strategy_grid_builds_rsi_crossdown_cooldown_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_mean_reversion_crossdown_cooldown",
                    "params": {
                        "period": [24],
                        "oversold": [19],
                        "overbought": [64],
                        "cooldown_bars": [2, 4],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {"period": 24, "oversold": 19, "overbought": 64, "cooldown_bars": 2},
        )
        self.assertEqual(
            strategies[1].parameters,
            {"period": 24, "oversold": 19, "overbought": 64, "cooldown_bars": 4},
        )

    def test_expand_strategy_grid_builds_bollinger_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "bollinger_mean_reversion",
                    "params": {
                        "period": [20],
                        "band_width": [1.5, 2.0],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(strategies[0].parameters, {"period": 20, "band_width": 1.5})
        self.assertEqual(strategies[1].parameters, {"period": 20, "band_width": 2.0})

    def test_expand_strategy_grid_builds_pattern_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "double_top_bottom_reversal",
                    "params": {
                        "swing_window": [2],
                        "min_separation_bars": [6, 8],
                        "max_separation_bars": [30],
                        "peak_tolerance_pct": [0.01],
                        "neckline_buffer_pct": [0.02],
                        "breakout_pct": [0.001],
                        "lookback_bars": [120],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "swing_window": 2,
                "min_separation_bars": 6,
                "max_separation_bars": 30,
                "peak_tolerance_pct": 0.01,
                "neckline_buffer_pct": 0.02,
                "breakout_pct": 0.001,
                "lookback_bars": 120,
            },
        )

    def test_expand_strategy_grid_builds_ema_trailing_exit_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "ema_triple_pullback_trailing_exit",
                    "params": {
                        "fast_window": [10],
                        "middle_window": [22],
                        "slow_window": [55],
                        "pullback_pct": [0.0025],
                        "trailing_window": [10, 14],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "fast_window": 10,
                "middle_window": 22,
                "slow_window": 55,
                "pullback_pct": 0.0025,
                "trailing_window": 10,
            },
        )
        self.assertEqual(
            strategies[1].parameters,
            {
                "fast_window": 10,
                "middle_window": 22,
                "slow_window": 55,
                "pullback_pct": 0.0025,
                "trailing_window": 14,
            },
        )

    def test_expand_strategy_grid_builds_multi_indicator_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_ema_atr_price_structure",
                    "params": {
                        "period": [24],
                        "oversold": [19],
                        "overbought": [64],
                        "ema_window": [100, 200],
                        "ema_slope_window": [6],
                        "atr_period": [14],
                        "min_atr_pct": [1.0],
                        "max_atr_pct": [4.0],
                        "structure_window": [20],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 24,
                "oversold": 19,
                "overbought": 64,
                "ema_window": 100,
                "ema_slope_window": 6,
                "atr_period": 14,
                "min_atr_pct": 1.0,
                "max_atr_pct": 4.0,
                "structure_window": 20,
            },
        )

    def test_expand_strategy_grid_builds_multi_indicator_atr_variant(self) -> None:
        strategies = expand_strategy_grid(
            [
                {
                    "name": "rsi_ema_atr_volatility_filter",
                    "params": {
                        "period": [24],
                        "oversold": [19],
                        "overbought": [64],
                        "ema_window": [100, 200],
                        "ema_slope_window": [6],
                        "atr_period": [14],
                        "min_atr_pct": [1.0],
                        "max_atr_pct": [4.0],
                    },
                }
            ]
        )

        self.assertEqual(len(strategies), 2)
        self.assertEqual(
            strategies[0].parameters,
            {
                "period": 24,
                "oversold": 19,
                "overbought": 64,
                "ema_window": 100,
                "ema_slope_window": 6,
                "atr_period": 14,
                "min_atr_pct": 1.0,
                "max_atr_pct": 4.0,
            },
        )


if __name__ == "__main__":
    unittest.main()
