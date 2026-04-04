from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from itertools import product
from pathlib import Path

from trading_strategy.backtest import run_backtest
from trading_strategy.data import load_ohlcv_csv
from trading_strategy.portfolio import compare_portfolio_from_config
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare trading strategies on historical CSV data.")
    parser.add_argument("--data", help="Path to OHLCV CSV file")
    parser.add_argument("--config", help="Path to experiment config JSON")
    parser.add_argument("--portfolio-config", help="Path to portfolio comparison config JSON")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--plot-output", help="Optional output SVG path for the top-ranked strategy chart")
    parser.add_argument(
        "--max-workers",
        type=int,
        help="Maximum number of strategies to backtest in parallel",
    )
    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help="Print the registered strategy catalog and exit",
    )
    args = parser.parse_args(argv)

    if args.list_strategies:
        _print_strategy_catalog()
        return 0

    if args.portfolio_config:
        if args.data or args.config:
            parser.error("--portfolio-config cannot be combined with --data or --config")
        if args.plot_output:
            parser.error("--plot-output is not supported with --portfolio-config")

        config = _load_json(args.portfolio_config)
        result = compare_portfolio_from_config(
            config,
            base_path=Path(args.portfolio_config).resolve().parent,
        )
        experiment = config.get("experiment", {})
        _print_portfolio_result(result, experiment)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "experiment": experiment,
                "portfolio": result.to_dict(),
            }
            output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        return 0

    if not args.data or not args.config:
        parser.error("--data and --config are required unless --list-strategies or --portfolio-config is used")

    config = _load_json(args.config)
    candles = load_ohlcv_csv(args.data)
    strategies = expand_strategy_grid(config["strategies"])
    risk_profiles = _expand_parameter_grid(config.get("risk_management"))
    ranking_metric = config.get("ranking_metric", "sharpe")
    experiment = config.get("experiment", {})
    max_workers = _resolve_max_workers(args.max_workers, config.get("max_workers"))

    tasks = _build_backtest_tasks(
        candles=candles,
        strategies=strategies,
        risk_profiles=risk_profiles,
        initial_cash=float(config.get("initial_cash", 10_000)),
        commission_bps=float(config.get("commission_bps", 0)),
        slippage_bps=float(config.get("slippage_bps", 0)),
        bars_per_year=int(config.get("bars_per_year", 252)),
    )
    results = _run_backtests(tasks, max_workers=max_workers)
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


def _build_backtest_tasks(
    *,
    candles,
    strategies,
    risk_profiles: list[dict],
    initial_cash: float,
    commission_bps: float,
    slippage_bps: float,
    bars_per_year: int,
) -> list[dict]:
    return [
        {
            "candles": candles,
            "strategy": strategy,
            "initial_cash": initial_cash,
            "commission_bps": commission_bps,
            "slippage_bps": slippage_bps,
            "bars_per_year": bars_per_year,
            "atr_period": _optional_int(risk_profile.get("atr_period")),
            "stop_loss_atr_multiple": _optional_float(risk_profile.get("stop_loss_atr_multiple")),
            "take_profit_atr_multiple": _optional_float(risk_profile.get("take_profit_atr_multiple")),
            "leverage": _optional_float(risk_profile.get("leverage")),
            "maintenance_margin_rate": _optional_float(risk_profile.get("maintenance_margin_rate")),
            "liquidation_fee_bps": _optional_float(risk_profile.get("liquidation_fee_bps")),
            "funding_rate_bps_per_bar": _optional_float(risk_profile.get("funding_rate_bps_per_bar")),
        }
        for strategy in strategies
        for risk_profile in risk_profiles
    ]


def _run_single_backtest(task: dict):
    return run_backtest(**task)


def _run_backtests(tasks: list[dict], *, max_workers: int):
    if max_workers == 1:
        return [_run_single_backtest(task) for task in tasks]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(_run_single_backtest, tasks))


def _resolve_max_workers(cli_value: int | None, config_value) -> int:
    raw_value = cli_value if cli_value is not None else config_value
    if raw_value is None:
        return 1

    max_workers = int(raw_value)
    if max_workers <= 0:
        raise ValueError("max_workers must be positive")
    return max_workers


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


def _print_portfolio_result(result, experiment: dict) -> None:
    if experiment:
        print(f"Portfolio experiment: {experiment.get('label', 'unnamed')}")
        if experiment.get("notes"):
            print(f"Notes: {experiment['notes']}")
    print("Portfolio metrics:")
    print(
        _row(
            (
                "total_return_pct",
                "annualized_return_pct",
                "max_drawdown_pct",
                "sharpe",
                "exposure_pct",
            )
        )
    )
    metrics = result.metrics.to_dict()
    print(
        _row(
            (
                _format_number(metrics["total_return_pct"]),
                _format_number(metrics["annualized_return_pct"]),
                _format_number(metrics["max_drawdown_pct"]),
                _format_number(metrics["sharpe"]),
                _format_number(metrics["exposure_pct"]),
            )
        )
    )
    print("Components:")
    print(_row(("label", "weight", "strategy", "params", "source_rank")))
    for component in result.components:
        print(
            _row(
                (
                    component.label,
                    _format_number(component.weight * 100),
                    component.strategy_name,
                    _format_params(component.parameters | component.execution_parameters),
                    str(component.result_rank),
                )
            )
        )


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
