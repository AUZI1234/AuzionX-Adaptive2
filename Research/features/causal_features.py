"""Causal tick features. Future-labelled excursions are deliberately separate."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from math import log, sqrt
from typing import Iterable
from Research.data.validate_ticks import Tick

@dataclass(frozen=True)
class FeatureRow:
    timestamp_utc: datetime
    short_return: float | None
    signed_tick: int
    spread: float
    tick_rate: float | None
    realized_volatility: float | None
    directional_efficiency: float | None
    velocity: float | None
    acceleration: float | None
    valid: bool


def causal_features(ticks: Iterable[Tick], window: int = 10) -> list[FeatureRow]:
    rows, history, velocities = [], deque(maxlen=window + 1), deque(maxlen=3)
    for tick in ticks:
        prior = history[-1] if history else None
        signed = 0 if prior is None or tick.mid == prior.mid else (1 if tick.mid > prior.mid else -1)
        ret = log(tick.mid / prior.mid) if prior and tick.mid > 0 and prior.mid > 0 else None
        elapsed = (tick.timestamp_utc - prior.timestamp_utc).total_seconds() if prior else None
        rate = (1.0 / elapsed) if elapsed and elapsed > 0 else None
        velocity = (ret / elapsed) if ret is not None and elapsed and elapsed > 0 else None
        acceleration = None
        if velocity is not None and velocities and elapsed and elapsed > 0: acceleration = (velocity - velocities[-1]) / elapsed
        returns = [log(b.mid / a.mid) for a, b in zip(history, list(history)[1:]) if a.mid > 0 and b.mid > 0]
        rv = sqrt(sum(value * value for value in returns)) if returns else None
        path = sum(abs(value) for value in returns)
        efficiency = abs(sum(returns)) / path if path else None
        rows.append(FeatureRow(tick.timestamp_utc, ret, signed, tick.spread, rate, rv, efficiency, velocity, acceleration, bool(prior)))
        history.append(tick)
        if velocity is not None: velocities.append(velocity)
    return rows
