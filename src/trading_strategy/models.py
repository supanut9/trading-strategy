from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Trade:
    entry_time: str
    exit_time: str
    entry_price: float
    exit_price: float
    units: float
    pnl: float
    return_pct: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Metrics:
    ending_equity: float
    total_return_pct: float
    annualized_return_pct: float
    max_drawdown_pct: float
    sharpe: float
    trade_count: int
    win_rate_pct: float
    profit_factor: float
    exposure_pct: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class BacktestResult:
    strategy_name: str
    parameters: dict
    execution_parameters: dict | None
    metrics: Metrics
    equity_curve: list[float]
    trades: list[Trade]

    def to_dict(self) -> dict:
        return {
            "strategy_name": self.strategy_name,
            "parameters": self.parameters,
            "execution_parameters": self.execution_parameters or {},
            "metrics": self.metrics.to_dict(),
            "equity_curve": self.equity_curve,
            "trades": [trade.to_dict() for trade in self.trades],
        }
