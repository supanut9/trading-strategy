from __future__ import annotations

from trading_strategy.metrics import compute_metrics
from trading_strategy.models import BacktestResult, Candle, Trade
from trading_strategy.strategies import Strategy
from trading_strategy.strategies.indicators import average_true_range


def run_backtest(
    candles: list[Candle],
    strategy: Strategy,
    *,
    initial_cash: float,
    commission_bps: float = 0.0,
    slippage_bps: float = 0.0,
    bars_per_year: int = 252,
    atr_period: int | None = None,
    stop_loss_atr_multiple: float | None = None,
    take_profit_atr_multiple: float | None = None,
) -> BacktestResult:
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")

    commission_rate = commission_bps / 10_000
    slippage_rate = slippage_bps / 10_000
    risk_enabled = stop_loss_atr_multiple is not None or take_profit_atr_multiple is not None
    if risk_enabled:
        if atr_period is None or atr_period <= 0:
            raise ValueError("atr_period must be positive when ATR-based exits are enabled")
        if stop_loss_atr_multiple is not None and stop_loss_atr_multiple <= 0:
            raise ValueError("stop_loss_atr_multiple must be positive")
        if take_profit_atr_multiple is not None and take_profit_atr_multiple <= 0:
            raise ValueError("take_profit_atr_multiple must be positive")

    cash = initial_cash
    units = 0.0
    in_position = False
    pending_entry: dict | None = None
    stop_price: float | None = None
    take_profit_price: float | None = None
    trades: list[Trade] = []
    equity_curve = [initial_cash]
    exposure_bars = 0

    for index in range(1, len(candles)):
        current_candle = candles[index]
        prior_signal = strategy.desired_position(index - 1, candles)
        bar_had_position = in_position

        if prior_signal == 1 and not in_position:
            if risk_enabled and index < atr_period + 1:
                equity_curve.append(cash)
                continue
            entry_fill = current_candle.open * (1 + slippage_rate)
            affordable_units = cash / (entry_fill * (1 + commission_rate))
            entry_notional = affordable_units * entry_fill
            entry_fee = entry_notional * commission_rate
            cash -= entry_notional + entry_fee
            units = affordable_units
            in_position = True
            pending_entry = {
                "time": current_candle.timestamp,
                "price": entry_fill,
                "units": units,
                "gross_cost": entry_notional + entry_fee,
            }
            if risk_enabled:
                entry_atr = _atr_for_entry(index, candles, atr_period)
                stop_price = (
                    entry_fill - (entry_atr * stop_loss_atr_multiple)
                    if stop_loss_atr_multiple is not None
                    else None
                )
                take_profit_price = (
                    entry_fill + (entry_atr * take_profit_atr_multiple)
                    if take_profit_atr_multiple is not None
                    else None
                )
            bar_had_position = True

        elif prior_signal == 0 and in_position:
            exit_fill = current_candle.open * (1 - slippage_rate)
            exit_notional = units * exit_fill
            exit_fee = exit_notional * commission_rate
            cash += exit_notional - exit_fee
            trades.append(
                Trade(
                    entry_time=pending_entry["time"],
                    exit_time=current_candle.timestamp,
                    entry_price=pending_entry["price"],
                    exit_price=exit_fill,
                    units=units,
                    pnl=(exit_notional - exit_fee) - pending_entry["gross_cost"],
                    return_pct=(((exit_notional - exit_fee) / pending_entry["gross_cost"]) - 1) * 100,
                )
            )
            units = 0.0
            in_position = False
            pending_entry = None
            stop_price = None
            take_profit_price = None

        if in_position and (stop_price is not None or take_profit_price is not None):
            risk_exit_level = None
            if stop_price is not None and current_candle.low <= stop_price:
                risk_exit_level = stop_price
            elif take_profit_price is not None and current_candle.high >= take_profit_price:
                risk_exit_level = take_profit_price

            if risk_exit_level is not None:
                exit_fill = risk_exit_level * (1 - slippage_rate)
                exit_notional = units * exit_fill
                exit_fee = exit_notional * commission_rate
                cash += exit_notional - exit_fee
                trades.append(
                    Trade(
                        entry_time=pending_entry["time"],
                        exit_time=current_candle.timestamp,
                        entry_price=pending_entry["price"],
                        exit_price=exit_fill,
                        units=units,
                        pnl=(exit_notional - exit_fee) - pending_entry["gross_cost"],
                        return_pct=(((exit_notional - exit_fee) / pending_entry["gross_cost"]) - 1) * 100,
                    )
                )
                units = 0.0
                in_position = False
                pending_entry = None
                stop_price = None
                take_profit_price = None

        mark_to_market = cash + (units * current_candle.close)
        equity_curve.append(mark_to_market)
        if bar_had_position or in_position:
            exposure_bars += 1
    if in_position:
        final_candle = candles[-1]
        exit_fill = final_candle.close * (1 - slippage_rate)
        exit_notional = units * exit_fill
        exit_fee = exit_notional * commission_rate
        cash += exit_notional - exit_fee
        trades.append(
            Trade(
                entry_time=pending_entry["time"],
                exit_time=final_candle.timestamp,
                entry_price=pending_entry["price"],
                exit_price=exit_fill,
                units=units,
                pnl=(exit_notional - exit_fee) - pending_entry["gross_cost"],
                return_pct=(((exit_notional - exit_fee) / pending_entry["gross_cost"]) - 1) * 100,
            )
        )
        units = 0.0
        equity_curve[-1] = cash

    metrics = compute_metrics(
        equity_curve=equity_curve,
        trades=trades,
        exposure_bars=exposure_bars,
        total_bars=len(candles) - 1,
        initial_cash=initial_cash,
        bars_per_year=bars_per_year,
    )

    return BacktestResult(
        strategy_name=strategy.name,
        parameters=strategy.parameters,
        execution_parameters={
            key: value
            for key, value in {
                "atr_period": atr_period,
                "stop_loss_atr_multiple": stop_loss_atr_multiple,
                "take_profit_atr_multiple": take_profit_atr_multiple,
            }.items()
            if value is not None
        },
        metrics=metrics,
        equity_curve=equity_curve,
        trades=trades,
    )


def _atr_for_entry(index: int, candles: list[Candle], period: int) -> float:
    history = candles[:index]
    highs = [candle.high for candle in history]
    lows = [candle.low for candle in history]
    closes = [candle.close for candle in history]
    return average_true_range(highs, lows, closes, period)
