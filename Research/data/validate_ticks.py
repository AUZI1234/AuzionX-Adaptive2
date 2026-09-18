"""Deterministic XAUUSD quote validation; no trading functionality."""
from __future__ import annotations
import csv, hashlib, json, math
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

@dataclass(frozen=True)
class Tick:
    timestamp_utc: datetime
    bid: float
    ask: float
    sequence: int | None = None

    @property
    def mid(self) -> float: return (self.bid + self.ask) / 2.0
    @property
    def spread(self) -> float: return self.ask - self.bid


def parse_timestamp(value: str) -> datetime:
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None: raise ValueError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def read_ticks(path: str | Path) -> list[Tick]:
    result: list[Tick] = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            result.append(Tick(parse_timestamp(row["timestamp_utc"]), float(row["bid"]), float(row["ask"]), int(row["sequence"]) if row.get("sequence") else None))
    return result


def validate_ticks(ticks: list[Tick], gap_seconds: float = 60.0) -> dict:
    errors, warnings, duplicates, collisions, gaps = [], [], 0, 0, 0
    previous = None
    seen = set()
    for index, tick in enumerate(ticks):
        key = (tick.timestamp_utc, tick.bid, tick.ask, tick.sequence)
        if key in seen: duplicates += 1
        seen.add(key)
        if not (math.isfinite(tick.bid) and math.isfinite(tick.ask)) or tick.bid <= 0 or tick.ask < tick.bid:
            errors.append({"index": index, "reason": "invalid_quote"})
        if previous is not None:
            if tick.timestamp_utc < previous.timestamp_utc: errors.append({"index": index, "reason": "out_of_order"})
            if tick.timestamp_utc == previous.timestamp_utc: collisions += 1
            delta = (tick.timestamp_utc - previous.timestamp_utc).total_seconds()
            if delta > gap_seconds: gaps += 1
        previous = tick
    return {"rows": len(ticks), "errors": errors, "warnings": warnings, "duplicates": duplicates, "timestamp_collisions": collisions, "gaps": gaps, "valid": not errors}


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
    return digest.hexdigest()


def write_report(report: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
