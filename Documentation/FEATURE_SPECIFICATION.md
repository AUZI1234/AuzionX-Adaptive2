# Causal Feature Specification

All feature values at event time `t` use only events with timestamp/order no later than `t`. A feature is invalid until its declared warm-up and quality requirements are met. Windows are configurable experiment parameters; this document does not select trading thresholds.

| Feature | Definition and calculation | Failure cases and tests |
|---|---|---|
| Short return | `mid[t]/mid[t-k]-1` for prior event/time horizon `k` | Missing prior, gap; test hand-calculated paths |
| Normalized return | Short return divided by lagged/causal volatility scale | Zero scale; test scale invariance |
| Directional persistence | Same-sign movement fraction, run statistics, and optional sign autocorrelation over prior window | Mostly neutral or too few moves; test alternating and monotonic paths |
| Tick rate | Valid observations per elapsed prior interval | Zero elapsed time; test collisions and gaps |
| Signed tick movement | `sign(mid[t]-mid[previous_valid])`, with zero as neutral | Duplicate/invalid quote; test up/down/flat |
| Spread | `ask[t]-bid[t]`, optionally divided by mid/volatility | Crossed/stale quote; test spikes and invalid quotes |
| Spread percentile | Causal empirical percentile of current spread against prior spread history | Insufficient history/regime shift; test rank boundaries |
| Volatility | Causal dispersion/range scale over prior observations or bars | Jumps and zero variance; test constant and jump series |
| Realized volatility | Square root of sum of squared prior log returns, with declared annualization policy | Missing returns/overflow; test known returns |
| Range | High-low over a completed causal aggregation interval or prior event window | Incomplete bar; test boundary semantics |
| Momentum | Signed displacement or regression slope over prior horizon | Collinear/short sample; test flat and trend series |
| Velocity | Causal return/displacement divided by elapsed time | Zero/irregular elapsed time; test timestamp collisions |
| Acceleration | Difference between previously available velocities divided by elapsed time | Derivative noise/missing history; test ramp and impulse |
| Deceleration | Negative change in signed velocity magnitude or signed acceleration against movement direction | Direction change ambiguity; test fading impulse |
| Directional efficiency | Absolute net displacement divided by gross path length over prior window | Zero path; test chop versus monotonic path |
| Impulse quality | Displacement divided by path/range/volatility, with components retained | Zero denominator; test spike and noisy path |
| Pullback depth | Counter-movement from causal impulse extreme divided by impulse displacement/range | No confirmed impulse; test intact and invalidated pullbacks |
| Movement duration | Elapsed time from causal movement start to current/end event; end is only known at a later event | End-label leakage; test online start/end state |
| Movement excursion | Maximum favourable displacement after a declared causal event, measured only in a future-labelled analysis table | Must never be an input at event time; test label timestamps |
| Adverse excursion | Maximum adverse displacement after a declared causal event, future label only | Same leakage boundary; test separation from features |
| Market-state transition | State at `t` versus prior state using causal evidence, persistence and hysteresis | Repainting/one-tick flips; test transition fixtures |

## Timestamp semantics

Feature timestamp `t` is the timestamp of the latest source event consumed. Future-labelled excursion fields belong only to outcome/label tables and must never enter a live feature snapshot or decision. Every output includes `valid`, `sample_count`, `source_start`, `source_end`, and `feature_version`.

## Test protocol

Each feature must have a hand-calculated fixture, boundary tests, insufficient-data tests, duplicate/out-of-order tests, gap tests where applicable, and a causality test: append a future event and verify the value at all earlier timestamps is unchanged.
