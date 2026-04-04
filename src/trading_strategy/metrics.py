from __future__ import annotations

import math

from trading_strategy.models import Metrics, Trade


def compute_metrics(
    equity_curve: list[float],
    trades: list[Trade],
    exposure_bars: int,
    total_bars: int,
    initial_cash: float,
    bars_per_year: int,
) -> Metrics:
    ending_equity = equity_curve[-1]
    total_return = (ending_equity / initial_cash) - 1
    annualized_return = _annualized_return(
        ending_equity=ending_equity,
        initial_cash=initial_cash,
        periods=max(1, len(equity_curve) - 1),
        bars_per_year=bars_per_year,
    )
    returns = _period_returns(equity_curve)
    sharpe = _sharpe_ratio(returns, bars_per_year)
    max_drawdown = _max_drawdown(equity_curve)
    trade_count = len(trades)
    win_count = sum(1 for trade in trades if trade.pnl > 0)
    win_rate = (win_count / trade_count) if trade_count else 0.0
    gross_profit = sum(trade.pnl for trade in trades if trade.pnl > 0)
    gross_loss = abs(sum(trade.pnl for trade in trades if trade.pnl < 0))
    profit_factor = gross_profit / gross_loss if gross_loss else (math.inf if gross_profit > 0 else 0.0)
    exposure = exposure_bars / total_bars if total_bars else 0.0

    return compute_equity_curve_metrics(
        equity_curve,
        initial_cash=initial_cash,
        bars_per_year=bars_per_year,
        exposure_pct=exposure * 100,
        trade_count=trade_count,
        win_rate_pct=win_rate * 100,
        profit_factor=profit_factor,
    )


def compute_equity_curve_metrics(
    equity_curve: list[float],
    *,
    initial_cash: float,
    bars_per_year: int,
    exposure_pct: float = 0.0,
    trade_count: int = 0,
    win_rate_pct: float = 0.0,
    profit_factor: float = 0.0,
) -> Metrics:
    ending_equity = equity_curve[-1]
    total_return = (ending_equity / initial_cash) - 1
    annualized_return = _annualized_return(
        ending_equity=ending_equity,
        initial_cash=initial_cash,
        periods=max(1, len(equity_curve) - 1),
        bars_per_year=bars_per_year,
    )
    returns = _period_returns(equity_curve)
    sharpe = _sharpe_ratio(returns, bars_per_year)
    max_drawdown = _max_drawdown(equity_curve)

    return Metrics(
        ending_equity=ending_equity,
        total_return_pct=total_return * 100,
        annualized_return_pct=annualized_return * 100,
        max_drawdown_pct=max_drawdown * 100,
        sharpe=sharpe,
        trade_count=trade_count,
        win_rate_pct=win_rate_pct,
        profit_factor=profit_factor,
        exposure_pct=exposure_pct,
    )


def _annualized_return(
    *,
    ending_equity: float,
    initial_cash: float,
    periods: int,
    bars_per_year: int,
) -> float:
    if initial_cash <= 0 or ending_equity <= 0:
        return -1.0
    return (ending_equity / initial_cash) ** (bars_per_year / periods) - 1


def _period_returns(equity_curve: list[float]) -> list[float]:
    returns: list[float] = []
    for previous, current in zip(equity_curve, equity_curve[1:]):
        if previous == 0:
            returns.append(0.0)
        else:
            returns.append((current / previous) - 1)
    return returns


def _sharpe_ratio(returns: list[float], bars_per_year: int) -> float:
    if not returns:
        return 0.0
    mean_return = sum(returns) / len(returns)
    variance = sum((value - mean_return) ** 2 for value in returns) / len(returns)
    std_dev = math.sqrt(variance)
    if std_dev == 0:
        return 0.0
    return (mean_return / std_dev) * math.sqrt(bars_per_year)


def _max_drawdown(equity_curve: list[float]) -> float:
    peak = equity_curve[0]
    max_drawdown = 0.0
    for equity in equity_curve:
        peak = max(peak, equity)
        if peak == 0:
            continue
        drawdown = (peak - equity) / peak
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown
