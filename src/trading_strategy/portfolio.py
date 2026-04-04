from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from trading_strategy.metrics import compute_equity_curve_metrics
from trading_strategy.models import Metrics


@dataclass(frozen=True)
class PortfolioComponent:
    label: str
    weight: float
    result_file: str
    result_rank: int
    strategy_name: str
    parameters: dict
    execution_parameters: dict
    metrics: dict
    equity_curve: list[float]

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
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    results = payload.get("results", [])
    if not results:
        raise ValueError(f"result file has no results: {result_path}")
    if result_rank > len(results):
        raise ValueError(f"result_rank {result_rank} out of range for {result_path}")

    selected_result = results[result_rank - 1]
    label = spec.get("label") or selected_result["strategy_name"]
    return PortfolioComponent(
        label=label,
        weight=weight,
        result_file=result_file,
        result_rank=result_rank,
        strategy_name=selected_result["strategy_name"],
        parameters=selected_result.get("parameters", {}),
        execution_parameters=selected_result.get("execution_parameters", {}),
        metrics=selected_result["metrics"],
        equity_curve=selected_result["equity_curve"],
    )


def _validate_weights(components: list[PortfolioComponent]) -> None:
    total_weight = sum(component.weight for component in components)
    if any(component.weight <= 0 for component in components):
        raise ValueError("portfolio component weights must be positive")
    if abs(total_weight - 1.0) > 1e-9:
        raise ValueError("portfolio component weights must sum to 1.0")


def _combine_equity_curves(components: list[PortfolioComponent], *, initial_cash: float) -> list[float]:
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
