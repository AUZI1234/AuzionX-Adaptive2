"""Deterministic XAUUSD quote validation; no trading functionality."""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from dataclasses import dataclass
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
    result = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp_utc", "bid", "ask"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"missing required columns: {sorted(required - set(reader.fieldnames or []))}")
        for row in reader:
            result.append(Tick(parse_timestamp(row["timestamp_utc"]), float(row["bid"]), float(row["ask"]), int(row["sequence"]) if row.get("sequence") else None))
    return result

def validate_ticks(ticks: list[Tick], gap_seconds: float = 60.0, max_spread: float | None = None) -> dict:
    errors, warnings, duplicates, collisions, gaps, zero_moves, abnormal_spreads, malformed = [], [], 0, 0, 0, 0, 0, 0
    previous = None; seen = set(); spreads = []
    for index, tick in enumerate(ticks):
        key = (tick.timestamp_utc, tick.bid, tick.ask, tick.sequence)
        if key in seen: duplicates += 1
        seen.add(key)
        finite = all(math.isfinite(value) for value in (tick.bid, tick.ask))
        if not finite or tick.bid <= 0 or tick.ask <= 0 or tick.ask < tick.bid:
            malformed += 1; errors.append({"index": index, "reason": "invalid_quote"})
        else:
            spreads.append(tick.spread)
            if previous is not None and tick.mid == previous.mid: zero_moves += 1
            if max_spread is not None and tick.spread > max_spread:
                abnormal_spreads += 1; warnings.append({"index": index, "reason": "abnormal_spread", "spread": tick.spread})
        if previous is not None:
            if tick.timestamp_utc < previous.timestamp_utc: errors.append({"index": index, "reason": "out_of_order"})
            if tick.timestamp_utc == previous.timestamp_utc: collisions += 1
            delta = (tick.timestamp_utc - previous.timestamp_utc).total_seconds()
            if delta > gap_seconds: gaps += 1
        previous = tick
    return {"rows": len(ticks), "errors": errors, "warnings": warnings, "duplicates": duplicates, "timestamp_collisions": collisions, "gaps": gaps, "zero_movement_ticks": zero_moves, "abnormal_spreads": abnormal_spreads, "malformed_records": malformed, "spread_min": min(spreads) if spreads else None, "spread_max": max(spreads) if spreads else None, "valid": not errors}

def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
    return digest.hexdigest()

def write_report(report: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical XAUUSD bid/ask CSV without modifying it")
    parser.add_argument("csv_path"); parser.add_argument("--report", required=True); parser.add_argument("--gap-seconds", type=float, default=60.0); parser.add_argument("--max-spread", type=float)
    args = parser.parse_args()
    try:
        ticks = read_ticks(args.csv_path)
        report = validate_ticks(ticks, args.gap_seconds, args.max_spread)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {"rows": 0, "valid": False, "errors": [{"reason": "malformed_input", "detail": str(exc)}], "warnings": [], "malformed_records": 1}
    report["source"] = str(args.csv_path); report["sha256"] = file_sha256(args.csv_path) if Path(args.csv_path).is_file() else None
    write_report(report, args.report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid"] else 1

if __name__ == "__main__": raise SystemExit(main())
