from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from trading_strategy.data import load_ohlcv_csv
from trading_strategy.metrics import compute_equity_curve_metrics
from trading_strategy.models import Metrics


@dataclass(frozen=True)
class PortfolioComponent:
    label: str
    weight: float
    result_file: str
    data_file: str | None
    result_rank: int
    strategy_name: str
    parameters: dict
    execution_parameters: dict
    metrics: dict
    equity_curve: list[float]
    timestamps: list[str] | None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PortfolioComparisonResult:
    metrics: Metrics
    equity_curve: list[float]
    components: list[PortfolioComponent]

    def to_dict(self) -> dict:
        return {
            "metrics": self.metrics.to_dict(),
            "equity_curve": self.equity_curve,
            "components": [component.to_dict() for component in self.components],
        }


def compare_portfolio_from_config(config: dict, *, base_path: Path) -> PortfolioComparisonResult:
    component_specs = config.get("components", [])
    if not component_specs:
        raise ValueError("portfolio config must include at least one component")

    initial_cash = float(config.get("initial_cash", 1_000))
    bars_per_year = int(config.get("bars_per_year", 252))
    components = [_load_component(spec, base_path=base_path) for spec in component_specs]

    _validate_weights(components)
    combined_equity_curve = _combine_equity_curves(components, initial_cash=initial_cash)
    weighted_exposure_pct = sum(component.weight * component.metrics.get("exposure_pct", 0.0) for component in components)
    metrics = compute_equity_curve_metrics(
        combined_equity_curve,
        initial_cash=initial_cash,
        bars_per_year=bars_per_year,
        exposure_pct=weighted_exposure_pct,
    )
    return PortfolioComparisonResult(
        metrics=metrics,
        equity_curve=combined_equity_curve,
        components=components,
    )


def _load_component(spec: dict, *, base_path: Path) -> PortfolioComponent:
    result_file = spec.get("result_file")
    if not result_file:
        raise ValueError("portfolio component missing result_file")

    result_rank = int(spec.get("result_rank", 1))
    if result_rank <= 0:
        raise ValueError("result_rank must be positive")

    weight = float(spec.get("weight", 0.0))
    result_path = base_path / result_file
    data_file = spec.get("data_file")
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    results = payload.get("results", [])
    if not results:
        raise ValueError(f"result file has no results: {result_path}")
    if result_rank > len(results):
        raise ValueError(f"result_rank {result_rank} out of range for {result_path}")

    selected_result = results[result_rank - 1]
    label = spec.get("label") or selected_result["strategy_name"]
    timestamps = None
    if data_file is not None:
        candles = load_ohlcv_csv(base_path / data_file)
        timestamps = [candle.timestamp for candle in candles]
        if len(timestamps) != len(selected_result["equity_curve"]):
            raise ValueError("component data_file must have the same number of rows as the result equity curve length")
    return PortfolioComponent(
        label=label,
        weight=weight,
        result_file=result_file,
        data_file=data_file,
        result_rank=result_rank,
        strategy_name=selected_result["strategy_name"],
        parameters=selected_result.get("parameters", {}),
        execution_parameters=selected_result.get("execution_parameters", {}),
        metrics=selected_result["metrics"],
        equity_curve=selected_result["equity_curve"],
        timestamps=timestamps,
    )


def _validate_weights(components: list[PortfolioComponent]) -> None:
    total_weight = sum(component.weight for component in components)
    if any(component.weight <= 0 for component in components):
        raise ValueError("portfolio component weights must be positive")
    if abs(total_weight - 1.0) > 1e-9:
        raise ValueError("portfolio component weights must sum to 1.0")


def _combine_equity_curves(components: list[PortfolioComponent], *, initial_cash: float) -> list[float]:
    if any(component.timestamps is not None for component in components):
        if any(component.timestamps is None for component in components):
            raise ValueError("all portfolio components must provide data_file when timestamp alignment is used")
        return _combine_equity_curves_by_timestamp(components, initial_cash=initial_cash)

    expected_length = len(components[0].equity_curve)
    if expected_length == 0:
        raise ValueError("portfolio component equity curves must not be empty")

    normalized_curves: list[list[float]] = []
    for component in components:
        if len(component.equity_curve) != expected_length:
            raise ValueError("portfolio components must use result files with matching equity curve lengths")
        starting_equity = component.equity_curve[0]
        if starting_equity <= 0:
            raise ValueError("portfolio component equity curves must start above zero")
        normalized_curves.append([value / starting_equity for value in component.equity_curve])

    combined_curve: list[float] = []
    for bar_index in range(expected_length):
        combined_normalized_equity = sum(
            component.weight * normalized_curves[index][bar_index]
            for index, component in enumerate(components)
        )
        combined_curve.append(initial_cash * combined_normalized_equity)
    return combined_curve


def _combine_equity_curves_by_timestamp(components: list[PortfolioComponent], *, initial_cash: float) -> list[float]:
    parsed_components = [_normalized_component_series(component) for component in components]
    overlap_start = max(series["timestamps"][0] for series in parsed_components)
    overlap_end = min(series["timestamps"][-1] for series in parsed_components)
    if overlap_start >= overlap_end:
        raise ValueError("portfolio components do not share an overlapping timestamp range")

    aligned_timestamps = sorted(
        {
            timestamp
            for series in parsed_components
            for timestamp in series["timestamps"]
            if overlap_start <= timestamp <= overlap_end
        }
    )
    if not aligned_timestamps:
        raise ValueError("portfolio components do not share any aligned timestamps")

    combined_curve: list[float] = []
    for timestamp in aligned_timestamps:
        combined_normalized_equity = 0.0
        for series in parsed_components:
            combined_normalized_equity += series["weight"] * _value_at_timestamp(series, timestamp)
        combined_curve.append(initial_cash * combined_normalized_equity)
    return combined_curve


def _normalized_component_series(component: PortfolioComponent) -> dict:
    timestamps = component.timestamps or []
    if not timestamps:
        raise ValueError("timestamp alignment requires component timestamps")
    if len(timestamps) != len(component.equity_curve):
        raise ValueError("component timestamps must match equity curve length")

    starting_equity = component.equity_curve[0]
    if starting_equity <= 0:
        raise ValueError("portfolio component equity curves must start above zero")
    normalized_curve = [value / starting_equity for value in component.equity_curve]
    return {
        "weight": component.weight,
        "timestamps": timestamps,
        "normalized_curve": normalized_curve,
    }


def _value_at_timestamp(series: dict, timestamp: str) -> float:
    timestamps = series["timestamps"]
    values = series["normalized_curve"]
    latest_value = values[0]
    for point_timestamp, value in zip(timestamps, values):
        if point_timestamp > timestamp:
            break
        latest_value = value
    return latest_value
