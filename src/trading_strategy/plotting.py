from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from trading_strategy.models import BacktestResult, Candle


def write_backtest_svg(
    candles: list[Candle],
    result: BacktestResult,
    output_path: str | Path,
    *,
    title: str | None = None,
    start_index: int | None = None,
    end_index: int | None = None,
    annotations: list[dict] | None = None,
) -> Path:
    if len(candles) != len(result.equity_curve):
        raise ValueError("candles and equity curve must have matching lengths")
    if len(candles) < 2:
        raise ValueError("at least two candles are required to plot")

    start = 0 if start_index is None else start_index
    end = (len(candles) - 1) if end_index is None else end_index
    if start < 0 or end < start or end >= len(candles):
        raise ValueError("invalid plot window")

    candles = candles[start : end + 1]
    equities = result.equity_curve[start : end + 1]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    width = 1400
    height = 900
    margin_left = 80
    margin_right = 40
    header_height = 110
    gap = 40
    price_height = 420
    equity_height = 180
    panel_width = width - margin_left - margin_right
    price_top = header_height
    equity_top = price_top + price_height + gap

    closes = [candle.close for candle in candles]
    candle_count = len(candles)

    entry_indices: list[tuple[int, float]] = []
    exit_indices: list[tuple[int, float]] = []
    timestamp_index = {candle.timestamp: index for index, candle in enumerate(candles)}
    for trade in result.trades:
        entry_index = timestamp_index.get(trade.entry_time)
        exit_index = timestamp_index.get(trade.exit_time)
        if entry_index is not None:
            entry_indices.append((entry_index, trade.entry_price))
        if exit_index is not None:
            exit_indices.append((exit_index, trade.exit_price))

    def x_scale(index: int) -> float:
        if candle_count == 1:
            return margin_left
        return margin_left + ((index / (candle_count - 1)) * panel_width)

    def y_scale(value: float, minimum: float, maximum: float, top: float, panel_height: float) -> float:
        if maximum == minimum:
            return top + (panel_height / 2)
        return top + ((maximum - value) / (maximum - minimum)) * panel_height

    price_min = min(candle.low for candle in candles)
    price_max = max(candle.high for candle in candles)
    equity_min = min(equities)
    equity_max = max(equities)

    price_line = _polyline_points(
        [
            (x_scale(index), y_scale(close, price_min, price_max, price_top, price_height))
            for index, close in enumerate(closes)
        ]
    )
    equity_line = _polyline_points(
        [
            (x_scale(index), y_scale(value, equity_min, equity_max, equity_top, equity_height))
            for index, value in enumerate(equities)
        ]
    )

    summary_title = title or result.strategy_name
    metrics = result.metrics
    summary = (
        f"Return {metrics.total_return_pct:.2f}% | "
        f"Max DD {metrics.max_drawdown_pct:.2f}% | "
        f"Sharpe {metrics.sharpe:.2f} | "
        f"Trades {metrics.trade_count} | "
        f"Win {metrics.win_rate_pct:.2f}%"
    )
    params = ", ".join(f"{key}={value}" for key, value in result.parameters.items()) or "-"
    start_label = _format_timestamp(candles[0].timestamp)
    end_label = _format_timestamp(candles[-1].timestamp)
    annotation_svg = _annotations_svg(
        annotations or [],
        x_scale,
        lambda value: y_scale(value, price_min, price_max, price_top, price_height),
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{margin_left}" y="36" font-size="26" font-family="Helvetica, Arial, sans-serif" fill="#111827">{escape(summary_title)}</text>
  <text x="{margin_left}" y="62" font-size="15" font-family="Helvetica, Arial, sans-serif" fill="#374151">{escape(summary)}</text>
  <text x="{margin_left}" y="84" font-size="13" font-family="Helvetica, Arial, sans-serif" fill="#6b7280">{escape(params)}</text>

  {_panel_background(margin_left, price_top, panel_width, price_height, "Price")}
  {_panel_background(margin_left, equity_top, panel_width, equity_height, "Equity")}

  {_axis_labels(margin_left, width - margin_right, price_top, price_height, price_min, price_max)}
  {_axis_labels(margin_left, width - margin_right, equity_top, equity_height, equity_min, equity_max)}

  <polyline fill="none" stroke="#2563eb" stroke-width="1.6" points="{price_line}"/>
  {annotation_svg}
  <polyline fill="none" stroke="#111827" stroke-width="1.6" points="{equity_line}"/>
  {_trade_markers(entry_indices, x_scale, lambda price: y_scale(price, price_min, price_max, price_top, price_height), "#16a34a", up=True)}
  {_trade_markers(exit_indices, x_scale, lambda price: y_scale(price, price_min, price_max, price_top, price_height), "#dc2626", up=False)}

  <text x="{margin_left}" y="{height - 18}" font-size="12" font-family="Helvetica, Arial, sans-serif" fill="#6b7280">{escape(start_label)}</text>
  <text x="{width - margin_right}" y="{height - 18}" font-size="12" text-anchor="end" font-family="Helvetica, Arial, sans-serif" fill="#6b7280">{escape(end_label)}</text>
</svg>
"""

    output.write_text(svg, encoding="utf-8")
    return output


def _polyline_points(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points)


def _panel_background(x: float, y: float, width: float, height: float, label: str) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#f8fafc" stroke="#d1d5db"/>'
        f'<text x="{x + 12}" y="{y + 22}" font-size="14" font-family="Helvetica, Arial, sans-serif" fill="#111827">{escape(label)}</text>'
    )


def _axis_labels(
    left: float,
    right: float,
    top: float,
    height: float,
    minimum: float,
    maximum: float,
) -> str:
    lines: list[str] = []
    for step in range(5):
        y = top + ((height / 4) * step)
        value = maximum - ((maximum - minimum) * (step / 4))
        lines.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" stroke="#e5e7eb" stroke-dasharray="3 4"/>'
        )
        lines.append(
            f'<text x="{left - 8}" y="{y + 4:.2f}" text-anchor="end" font-size="11" '
            f'font-family="Helvetica, Arial, sans-serif" fill="#6b7280">{value:.2f}</text>'
        )
    return "".join(lines)


def _trade_markers(
    trades: list[tuple[int, float]],
    x_scale,
    y_scale,
    color: str,
    *,
    up: bool,
) -> str:
    markers: list[str] = []
    for index, price in trades:
        x = x_scale(index)
        y = y_scale(price)
        if up:
            points = f"{x:.2f},{y - 8:.2f} {x - 6:.2f},{y + 4:.2f} {x + 6:.2f},{y + 4:.2f}"
        else:
            points = f"{x:.2f},{y + 8:.2f} {x - 6:.2f},{y - 4:.2f} {x + 6:.2f},{y - 4:.2f}"
        markers.append(f'<polygon points="{points}" fill="{color}" opacity="0.9"/>')
    return "".join(markers)


def _annotations_svg(annotations: list[dict], x_scale, y_scale) -> str:
    elements: list[str] = []
    for annotation in annotations:
        kind = annotation.get("kind")
        color = annotation.get("color", "#7c3aed")
        if kind == "point":
            x = x_scale(annotation["index"])
            y = y_scale(annotation["value"])
            label = escape(annotation.get("label", ""))
            elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{color}" stroke="#ffffff" stroke-width="1.5"/>')
            if label:
                elements.append(
                    f'<text x="{x + 8:.2f}" y="{y - 8:.2f}" font-size="12" font-family="Helvetica, Arial, sans-serif" fill="{color}">{label}</text>'
                )
        elif kind == "horizontal_line":
            x1 = x_scale(annotation["start_index"])
            x2 = x_scale(annotation["end_index"])
            y = y_scale(annotation["value"])
            label = escape(annotation.get("label", ""))
            elements.append(
                f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{color}" stroke-width="1.4" stroke-dasharray="6 4"/>'
            )
            if label:
                elements.append(
                    f'<text x="{x2 - 4:.2f}" y="{y - 8:.2f}" text-anchor="end" font-size="12" font-family="Helvetica, Arial, sans-serif" fill="{color}">{label}</text>'
                )
        elif kind == "box_text":
            x = annotation.get("x", 96)
            y = annotation.get("y", 118)
            lines = annotation.get("lines", [])
            box_height = 18 + (len(lines) * 16)
            elements.append(
                f'<rect x="{x}" y="{y}" width="240" height="{box_height}" rx="8" fill="#ffffff" stroke="{color}" opacity="0.92"/>'
            )
            for idx, line in enumerate(lines):
                elements.append(
                    f'<text x="{x + 10}" y="{y + 18 + (idx * 15)}" font-size="12" font-family="Helvetica, Arial, sans-serif" fill="#111827">{escape(str(line))}</text>'
                )
    return "".join(elements)


def _format_timestamp(raw: str) -> str:
    try:
        if raw.isdigit():
            timestamp = int(raw)
            if len(raw) >= 13:
                dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
            else:
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        pass
    return raw
