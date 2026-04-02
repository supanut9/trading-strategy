from __future__ import annotations

import csv
from pathlib import Path

from trading_strategy.models import Candle


REQUIRED_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


def load_ohlcv_csv(path: str | Path) -> list[Candle]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

        candles: list[Candle] = []
        for row_number, row in enumerate(reader, start=2):
            try:
                candles.append(
                    Candle(
                        timestamp=row["timestamp"],
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value on row {row_number}") from exc

    if len(candles) < 2:
        raise ValueError("At least two rows of market data are required")

    return candles
