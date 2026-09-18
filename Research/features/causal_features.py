"""Causal tick features. Future-labelled excursions are deliberately separate."""
from __future__ import annotations
import argparse, csv, json
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime
from math import log, sqrt
from typing import Iterable
from Research.data.validate_ticks import Tick, read_ticks

@dataclass(frozen=True)
class FeatureRow:
    timestamp_utc: datetime; short_return: float | None; signed_tick: int; spread: float
    tick_rate: float | None; realized_volatility: float | None; directional_efficiency: float | None
    velocity: float | None; acceleration: float | None; valid: bool

def causal_features(ticks: Iterable[Tick], window: int = 10) -> list[FeatureRow]:
    rows=[]; history=deque(maxlen=window + 1); velocities=deque(maxlen=3)
    for tick in ticks:
        prior = history[-1] if history else None
        signed = 0 if prior is None or tick.mid == prior.mid else (1 if tick.mid > prior.mid else -1)
        ret = log(tick.mid / prior.mid) if prior and tick.mid > 0 and prior.mid > 0 else None
        elapsed = (tick.timestamp_utc - prior.timestamp_utc).total_seconds() if prior else None
        rate = (1.0 / elapsed) if elapsed and elapsed > 0 else None
        velocity = (ret / elapsed) if ret is not None and elapsed and elapsed > 0 else None
        acceleration = ((velocity - velocities[-1]) / elapsed) if velocity is not None and velocities and elapsed and elapsed > 0 else None
        prior_returns = [log(b.mid / a.mid) for a, b in zip(history, list(history)[1:]) if a.mid > 0 and b.mid > 0]
        # The current return is deliberately excluded: this snapshot's history is strictly prior data.
        rv = sqrt(sum(value * value for value in prior_returns)) if prior_returns else None
        path = sum(abs(value) for value in prior_returns)
        efficiency = abs(sum(prior_returns)) / path if path else None
        rows.append(FeatureRow(tick.timestamp_utc, ret, signed, tick.spread, rate, rv, efficiency, velocity, acceleration, bool(prior)))
        history.append(tick)
        if velocity is not None: velocities.append(velocity)
    return rows

def main() -> int:
    parser=argparse.ArgumentParser(description="Generate causal feature CSV; no signals or orders")
    parser.add_argument("csv_path"); parser.add_argument("--output", required=True); parser.add_argument("--window", type=int, default=10)
    args=parser.parse_args(); rows=causal_features(read_ticks(args.csv_path), args.window)
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer=csv.DictWriter(handle, fieldnames=[field.name for field in FeatureRow.__dataclass_fields__.values()]); writer.writeheader()
        for row in rows:
            record=asdict(row); record["timestamp_utc"]=record["timestamp_utc"].isoformat(); writer.writerow(record)
    print(json.dumps({"rows": len(rows), "output": args.output}, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
