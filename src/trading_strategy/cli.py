from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from trading_strategy.backtest import run_backtest
from trading_strategy.data import load_ohlcv_csv
from trading_strategy.plotting import write_backtest_svg
from trading_strategy.strategies import available_strategies, expand_strategy_grid


DEFAULT_COLUMNS = (
    "rank",
    "strategy",
    "params",
    "total_return_pct",
    "annualized_return_pct",
    "max_drawdown_pct",
    "sharpe",
    "trade_count",
    "win_rate_pct",
    "exposure_pct",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare trading strategies on historical CSV data.")
    parser.add_argument("--data", help="Path to OHLCV CSV file")
    parser.add_argument("--config", help="Path to experiment config JSON")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--plot-output", help="Optional output SVG path for the top-ranked strategy chart")
    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help="Print the registered strategy catalog and exit",
    )
    args = parser.parse_args()

    if args.list_strategies:
        _print_strategy_catalog()
        return 0

    if not args.data or not args.config:
        parser.error("--data and --config are required unless --list-strategies is used")

    config = _load_json(args.config)
    candles = load_ohlcv_csv(args.data)
    strategies = expand_strategy_grid(config["strategies"])
    risk_profiles = _expand_parameter_grid(config.get("risk_management"))
    ranking_metric = config.get("ranking_metric", "sharpe")
    experiment = config.get("experiment", {})

    results = [
        run_backtest(
            candles,
            strategy,
            initial_cash=float(config.get("initial_cash", 10_000)),
            commission_bps=float(config.get("commission_bps", 0)),
            slippage_bps=float(config.get("slippage_bps", 0)),
            bars_per_year=int(config.get("bars_per_year", 252)),
            atr_period=_optional_int(risk_profile.get("atr_period")),
            stop_loss_atr_multiple=_optional_float(risk_profile.get("stop_loss_atr_multiple")),
            take_profit_atr_multiple=_optional_float(risk_profile.get("take_profit_atr_multiple")),
        )
        for strategy in strategies
        for risk_profile in risk_profiles
    ]
    results.sort(key=lambda result: _metric_value(result.to_dict()["metrics"], ranking_metric), reverse=True)

    _print_ranked_results(results, ranking_metric, experiment)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "experiment": experiment,
            "ranking_metric": ranking_metric,
            "results": [result.to_dict() for result in results],
        }
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if args.plot_output:
        title = (
            f"{experiment.get('label', 'Strategy Chart')} | "
            f"{results[0].strategy_name} | "
            f"{_display_parameters(results[0])}"
        )
        write_backtest_svg(candles, results[0], args.plot_output, title=title)

    return 0


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _expand_parameter_grid(spec: dict | None) -> list[dict]:
    if not spec:
        return [{}]

    normalized_items = {
        key: value if isinstance(value, list) else [value]
        for key, value in spec.items()
    }
    keys = list(normalized_items.keys())
    value_sets = [normalized_items[key] for key in keys]
    profiles: list[dict] = []
    for combination in product(*value_sets):
        profiles.append(dict(zip(keys, combination, strict=True)))
    return profiles


def _metric_value(metrics: dict, name: str) -> float:
    value = metrics.get(name)
    if value is None:
        raise ValueError(f"Unknown ranking metric: {name}")
    return float(value)


def _print_ranked_results(results: list, ranking_metric: str, experiment: dict) -> None:
    if experiment:
        print(f"Experiment: {experiment.get('label', 'unnamed')}")
        if experiment.get("symbol") or experiment.get("market_type") or experiment.get("timeframe"):
            print(
                "Market: "
                f"{experiment.get('symbol', '?')} "
                f"{experiment.get('market_type', '?')} "
                f"{experiment.get('timeframe', '?')}"
            )
    print(f"Ranking metric: {ranking_metric}")
    print(_row(DEFAULT_COLUMNS))
    for index, result in enumerate(results, start=1):
        metrics = result.metrics.to_dict()
        row = (
            str(index),
            result.strategy_name,
            _display_parameters(result),
            _format_number(metrics["total_return_pct"]),
            _format_number(metrics["annualized_return_pct"]),
            _format_number(metrics["max_drawdown_pct"]),
            _format_number(metrics["sharpe"]),
            str(metrics["trade_count"]),
            _format_number(metrics["win_rate_pct"]),
            _format_number(metrics["exposure_pct"]),
        )
        print(_row(row))


def _row(values: tuple[str, ...] | tuple) -> str:
    return " | ".join(f"{str(value):>18}" for value in values)


def _format_params(params: dict) -> str:
    if not params:
        return "-"
    return ",".join(f"{key}={value}" for key, value in params.items())


def _display_parameters(result) -> str:
    merged = dict(result.parameters)
    if result.execution_parameters:
        merged.update(result.execution_parameters)
    return _format_params(merged)


def _optional_int(value):
    return None if value is None else int(value)


def _optional_float(value):
    return None if value is None else float(value)


def _format_number(value: float) -> str:
    if value == float("inf"):
        return "inf"
    return f"{value:.2f}"


def _print_strategy_catalog() -> None:
    print("Available strategies:")
    for definition in available_strategies():
        print(f"- {definition.family}/{definition.name}: {definition.description}")


if __name__ == "__main__":
    raise SystemExit(main())
