# AuzionX Adaptive v2 — Testing and Validation Plan

## Required layers

1. **Unit/property:** formulas, rolling windows, normalization, causal swings, zero-tick policy, state hysteresis, score decomposition, sizing, exposure and cooldowns.
2. **Event replay:** deterministic bid/ask tick replay with duplicates, out-of-order data, gaps, missing ticks, restarts and broker events; assert no future read.
3. **Execution simulation:** realistic spread/commission/slippage/latency, fills, rejects, partial fills, stops/freeze levels, margin, netting and hedging.
4. **Historical research:** chronological development, validation and untouched test periods using the highest-quality available data; no leakage or survivorship bias.
5. **Walk-forward:** fit/select on a rolling or expanding development block, freeze, evaluate the next block; nested selection for competing variants.
6. **Stress/robustness:** worse costs, delay, spread shock, gap, volatility regimes, sessions, broker constraints, parameter perturbation and Monte Carlo where appropriate.
7. **Demo rehearsal:** verify reconciliation, telemetry, locks and order behaviour without live-money approval.

## Feature and state protocol

For each feature document observation, hypothesis, causal formula, null, sample size, missing policy, leakage risk, development result, validation result, untouched result, sensitivity, ablation and failure modes. For each state test entry, exit, dwell, hysteresis, timeout, insufficient-data and abnormal override. State labels must never place an order alone.

## Metrics and gates

Report net/gross expectancy per opportunity and risk unit, uncertainty intervals, return distribution, MAE/MFE tails, drawdown magnitude/duration, loss streak, exposure time, turnover, trade count as descriptive only, cost fraction, slippage/fill/reject rates, calibration, state/session/volatility slices and low-sample warnings. Build fails if an order bypasses risk, exceeds aggregate exposure, lacks protection, duplicates, retries non-idempotently, trades during a lock, widens a stop, or uses future information.

## ML gate

Use time-based train/validation/test and embargo overlapping labels. Compare to frozen deterministic and simple statistical baselines under identical causal features and costs. Require calibration, drift/support detection, reproducibility, ablation, fallback and predeclared improvement. ML cannot override risk or execution controls. Current status: evidence insufficient; requires testing.

## Test evidence record

Record dataset/source and exact dates, broker/symbol specification, timezone, feature/parameter/model/code versions, labels/horizons, split, search budget, cost/slippage/latency assumptions, sample size, uncertainty, ablations, failure cases and retain/reject decision. Never overwrite prior experiments.
