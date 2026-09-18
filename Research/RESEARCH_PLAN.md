# AuzionX Adaptive v2 — Research Plan

**Status:** architecture-review branch; no final EA; no live approval; no profitability claim.

## Phase 0: specification and data audit

Freeze event schema, timestamp and clock policy, bid/ask requirements, symbol contract, zero-tick/dedup policy, session calendar and versioned feature definitions. Acquire high-quality XAUUSD tick data. Measure gaps, duplicates, ordering, spread, tick-rate, contract changes and missing fields. Produce a data-quality report before strategy selection.

## Phase 1: market description

Measure distributions of return, range, volatility, volatility-of-volatility, spread, tick rate, directional runs, persistence, acceleration, breakouts, pullbacks, rejection and exhaustion by session, volatility regime and period. These are observations, not evidence of edge. Predeclare minimum samples and uncertainty methods.

## Phase 2: causal feature studies

Implement replay-safe feature generators and properties. For each feature test forward return, favourable/adverse excursion and cost-adjusted outcomes at predeclared horizons. Use development-only conditional analysis, monotonicity, stability, null comparisons and ablation. Freeze definitions before validation; do not label with future information at decision time.

## Phase 3: deterministic baseline

Build the simplest causal state machine, independent long/short evidence ledger, cost model and hard risk interface. Compare no-trade and simple directional benchmarks. Select windows, hysteresis, score weights and thresholds with nested walk-forward development and complexity control. Evaluate net costs, drawdown, exposure and state-conditional behaviour.

## Phase 4: mode and execution research

Test core, scalp and micro-flow as separate horizons under one aggregate budget. Replay broker-specific spread, latency, commission, slippage, fill, rejection, stop/freeze and restart behaviour. Measure assumed versus realized cost. Disable modes without stable net evidence; activity is not success.

## Phase 5: robustness and review

Run untouched periods, rolling walk-forward, parameter perturbation, cost/latency stress, spread shocks, gaps, sessions, volatility regimes, broker changes and adversarial failure sequences. Maintain an experiment registry with hypotheses, observations, inferences and measured results. Require architecture, quant, risk and execution review.

## Phase 6: optional ML challenger

Only after the deterministic baseline is reproducible, define one target such as calibrated probability of net favourable excursion. Freeze causal features, time splits, embargo, model class, calibration, drift support and fallback. Compare against deterministic and simple statistical baselines. Reject ML if improvement is not robust, cost-inclusive and maintained under regime stress.

## Experiment record

Every run records hypothesis; observation/inference/result; exact data dates/source; broker and symbol specification; code/feature/parameter versions; labels and horizons; development/validation/test split; search budget; cost, latency and slippage assumptions; sample size; metrics and uncertainty; ablations; failure cases; decision. Preserve all records.

## Exit criteria before EA

A replay engine, feature catalogue, deterministic baseline, execution-cost report, state-transition report, risk stress report, walk-forward report and reproducible evidence must exist. All safety invariants must pass and unresolved assumptions must be explicitly accepted by review. EA implementation and demo evaluation are later phases; live deployment remains separately prohibited.
