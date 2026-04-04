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
    leverage: float | None = None,
    maintenance_margin_rate: float | None = None,
    liquidation_fee_bps: float | None = None,
    funding_rate_bps_per_bar: float | None = None,
) -> BacktestResult:
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")

    commission_rate = commission_bps / 10_000
    slippage_rate = slippage_bps / 10_000
    liquidation_fee_rate = (liquidation_fee_bps or 0.0) / 10_000
    funding_rate_per_bar = (funding_rate_bps_per_bar or 0.0) / 10_000
    futures_enabled = leverage is not None
    risk_enabled = stop_loss_atr_multiple is not None or take_profit_atr_multiple is not None
    if futures_enabled:
        if leverage is None or leverage <= 1:
            raise ValueError("leverage must be greater than 1 when futures mode is enabled")
        if maintenance_margin_rate is None or maintenance_margin_rate < 0:
            raise ValueError("maintenance_margin_rate must be provided and non-negative in futures mode")
        if liquidation_fee_bps is not None and liquidation_fee_bps < 0:
            raise ValueError("liquidation_fee_bps must be non-negative")
    if risk_enabled:
        if atr_period is None or atr_period <= 0:
            raise ValueError("atr_period must be positive when ATR-based exits are enabled")
        if stop_loss_atr_multiple is not None and stop_loss_atr_multiple <= 0:
            raise ValueError("stop_loss_atr_multiple must be positive")
        if take_profit_atr_multiple is not None and take_profit_atr_multiple <= 0:
            raise ValueError("take_profit_atr_multiple must be positive")

    cash = initial_cash
    units = 0.0
    position_side = 0
    pending_entry: dict | None = None
    stop_price: float | None = None
    take_profit_price: float | None = None
    liquidation_price: float | None = None
    trades: list[Trade] = []
    equity_curve = [initial_cash]
    exposure_bars = 0

    for index in range(1, len(candles)):
        current_candle = candles[index]
        target_position = _interpret_signal(strategy, strategy.desired_position(index - 1, candles))
        bar_had_position = position_side != 0

        if target_position is not None and target_position != position_side and position_side != 0:
            exit_fill = _exit_fill_for_side(current_candle.open, slippage_rate, position_side)
            cash, trade = _close_position(
                cash=cash,
                units=units,
                position_side=position_side,
                entry=pending_entry,
                exit_fill=exit_fill,
                exit_time=current_candle.timestamp,
                commission_rate=commission_rate,
                futures_enabled=futures_enabled,
                liquidation_fee_rate=0.0,
            )
            trades.append(trade)
            units, position_side, pending_entry, stop_price, take_profit_price, liquidation_price = (
                _reset_open_position_state()
            )

        if target_position in (-1, 1) and position_side == 0:
            if risk_enabled and index < atr_period + 1:
                equity_curve.append(cash)
                continue
            entry_fill = _entry_fill_for_side(current_candle.open, slippage_rate, target_position)
            entry_equity = cash
            if futures_enabled:
                entry_notional = entry_equity * leverage
                affordable_units = entry_notional / entry_fill
            else:
                if target_position != 1:
                    raise ValueError("short positions require futures mode")
                affordable_units = cash / (entry_fill * (1 + commission_rate))
                entry_notional = affordable_units * entry_fill
            entry_fee = entry_notional * commission_rate
            if futures_enabled:
                cash -= entry_fee
                liquidation_price = _liquidation_price(entry_fill, leverage, maintenance_margin_rate, target_position)
            else:
                cash -= entry_notional + entry_fee
            units = affordable_units
            position_side = target_position
            pending_entry = {
                "time": current_candle.timestamp,
                "price": entry_fill,
                "units": units,
                "gross_cost": entry_notional + entry_fee,
                "starting_equity": entry_equity,
                "side": _side_label(target_position),
            }
            if risk_enabled:
                entry_atr = _atr_for_entry(index, candles, atr_period)
                stop_price = _risk_price(entry_fill, entry_atr, stop_loss_atr_multiple, target_position, stop=True)
                take_profit_price = _risk_price(
                    entry_fill,
                    entry_atr,
                    take_profit_atr_multiple,
                    target_position,
                    stop=False,
                )
            bar_had_position = True

        if position_side != 0 and futures_enabled and funding_rate_per_bar != 0:
            funding_payment = position_side * units * current_candle.close * funding_rate_per_bar
            cash -= funding_payment

        if position_side != 0 and (stop_price is not None or take_profit_price is not None):
            risk_exit_level = None
            if _stop_price_hit(current_candle, stop_price, position_side):
                risk_exit_level = stop_price
            elif _take_profit_hit(current_candle, take_profit_price, position_side):
                risk_exit_level = take_profit_price

            if risk_exit_level is not None:
                exit_fill = _exit_fill_for_side(risk_exit_level, slippage_rate, position_side)
                cash, trade = _close_position(
                    cash=cash,
                    units=units,
                    position_side=position_side,
                    entry=pending_entry,
                    exit_fill=exit_fill,
                    exit_time=current_candle.timestamp,
                    commission_rate=commission_rate,
                    futures_enabled=futures_enabled,
                    liquidation_fee_rate=0.0,
                )
                trades.append(trade)
                units, position_side, pending_entry, stop_price, take_profit_price, liquidation_price = (
                    _reset_open_position_state()
                )

        if _liquidation_hit(current_candle, liquidation_price, position_side, futures_enabled):
            cash, trade = _close_position(
                cash=cash,
                units=units,
                position_side=position_side,
                entry=pending_entry,
                exit_fill=liquidation_price,
                exit_time=current_candle.timestamp,
                commission_rate=commission_rate,
                futures_enabled=True,
                liquidation_fee_rate=liquidation_fee_rate,
            )
            cash = max(0.0, cash)
            trades.append(trade)
            units, position_side, pending_entry, stop_price, take_profit_price, liquidation_price = (
                _reset_open_position_state()
            )

        mark_to_market = _mark_to_market_equity(
            cash=cash,
            units=units,
            position_side=position_side,
            current_close=current_candle.close,
            entry=pending_entry,
            futures_enabled=futures_enabled,
        )
        equity_curve.append(mark_to_market)
        if bar_had_position or position_side != 0:
            exposure_bars += 1
    if position_side != 0:
        final_candle = candles[-1]
        exit_fill = _exit_fill_for_side(final_candle.close, slippage_rate, position_side)
        cash, trade = _close_position(
            cash=cash,
            units=units,
            position_side=position_side,
            entry=pending_entry,
            exit_fill=exit_fill,
            exit_time=final_candle.timestamp,
            commission_rate=commission_rate,
            futures_enabled=futures_enabled,
            liquidation_fee_rate=0.0,
        )
        trades.append(trade)
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
                "leverage": leverage,
                "maintenance_margin_rate": maintenance_margin_rate,
                "liquidation_fee_bps": liquidation_fee_bps,
                "funding_rate_bps_per_bar": funding_rate_bps_per_bar,
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


def _close_position(
    *,
    cash: float,
    units: float,
    position_side: int,
    entry: dict,
    exit_fill: float,
    exit_time: str,
    commission_rate: float,
    futures_enabled: bool,
    liquidation_fee_rate: float,
) -> tuple[float, Trade]:
    exit_notional = units * exit_fill
    exit_fee = exit_notional * (commission_rate + liquidation_fee_rate)
    if futures_enabled:
        starting_equity = entry["starting_equity"]
        pnl = position_side * units * (exit_fill - entry["price"])
        cash_after_exit = cash + pnl - exit_fee
        trade_pnl = cash_after_exit - starting_equity
        return_pct = ((cash_after_exit / starting_equity) - 1) * 100 if starting_equity else 0.0
        return cash_after_exit, Trade(
            entry_time=entry["time"],
            exit_time=exit_time,
            side=entry["side"],
            entry_price=entry["price"],
            exit_price=exit_fill,
            units=units,
            pnl=trade_pnl,
            return_pct=return_pct,
        )

    cash_after_exit = cash + exit_notional - exit_fee
    trade_pnl = (exit_notional - exit_fee) - entry["gross_cost"]
    return_pct = (((exit_notional - exit_fee) / entry["gross_cost"]) - 1) * 100 if entry["gross_cost"] else 0.0
    return cash_after_exit, Trade(
        entry_time=entry["time"],
        exit_time=exit_time,
        side=entry["side"],
        entry_price=entry["price"],
        exit_price=exit_fill,
        units=units,
        pnl=trade_pnl,
        return_pct=return_pct,
    )


def _mark_to_market_equity(
    *,
    cash: float,
    units: float,
    position_side: int,
    current_close: float,
    entry: dict | None,
    futures_enabled: bool,
) -> float:
    if not entry or units == 0:
        return cash
    if futures_enabled:
        return cash + (position_side * units * (current_close - entry["price"]))
    return cash + (units * current_close)


def _reset_open_position_state() -> tuple[float, int, None, None, None, None]:
    return 0.0, 0, None, None, None, None


def _interpret_signal(strategy: Strategy, raw_signal: int) -> int | None:
    if strategy.supports_short_positions:
        if raw_signal == 2:
            return None
        if raw_signal not in (-1, 0, 1):
            raise ValueError(f"Unsupported target-position signal: {raw_signal}")
        return raw_signal

    if raw_signal == -1:
        return None
    if raw_signal not in (0, 1):
        raise ValueError(f"Unsupported legacy signal: {raw_signal}")
    return raw_signal


def _entry_fill_for_side(price: float, slippage_rate: float, position_side: int) -> float:
    return price * (1 + slippage_rate) if position_side == 1 else price * (1 - slippage_rate)


def _exit_fill_for_side(price: float, slippage_rate: float, position_side: int) -> float:
    return price * (1 - slippage_rate) if position_side == 1 else price * (1 + slippage_rate)


def _liquidation_price(entry_fill: float, leverage: float, maintenance_margin_rate: float, position_side: int) -> float:
    if position_side == 1:
        return entry_fill * (1 - (1 / leverage) + maintenance_margin_rate)
    return entry_fill * (1 + (1 / leverage) - maintenance_margin_rate)


def _risk_price(
    entry_fill: float,
    entry_atr: float,
    multiple: float | None,
    position_side: int,
    *,
    stop: bool,
) -> float | None:
    if multiple is None:
        return None
    distance = entry_atr * multiple
    if position_side == 1:
        return entry_fill - distance if stop else entry_fill + distance
    return entry_fill + distance if stop else entry_fill - distance


def _stop_price_hit(candle: Candle, stop_price: float | None, position_side: int) -> bool:
    if stop_price is None:
        return False
    if position_side == 1:
        return candle.low <= stop_price
    return candle.high >= stop_price


def _take_profit_hit(candle: Candle, take_profit_price: float | None, position_side: int) -> bool:
    if take_profit_price is None:
        return False
    if position_side == 1:
        return candle.high >= take_profit_price
    return candle.low <= take_profit_price


def _liquidation_hit(
    candle: Candle,
    liquidation_price: float | None,
    position_side: int,
    futures_enabled: bool,
) -> bool:
    if not futures_enabled or position_side == 0 or liquidation_price is None:
        return False
    if position_side == 1:
        return candle.low <= liquidation_price
    return candle.high >= liquidation_price


def _side_label(position_side: int) -> str:
    return "long" if position_side == 1 else "short"
