# AuzionX Adaptive v2 — Strategy Blueprint

## Decision contract

Every causal evaluation produces `BUY`, `SELL`, or `WAIT`. WAIT is the initial and fail-closed result. The strategy is movement-led: it can participate in trends, momentum, acceleration, pullbacks, breakouts, continuation, micro-flow and exhaustion/reversal conditions, but none is a mandatory named setup. A state describes behaviour; an opportunity is a cost-adjusted, risk-approved intent.

## Evidence model

Maintain separate long and short ledgers. Evidence includes state compatibility, structure, flow imbalance/persistence, multi-horizon momentum, acceleration, volatility-scaled displacement, execution quality and expected favourable/adverse movement. Contradiction, uncertainty, spread, fees, slippage, latency and thesis overlap are penalties. Direction is selected only when its calibrated expected value exceeds the conservative all-in cost and the competing direction is materially weaker. Otherwise WAIT.

No threshold, window or weight is fixed because it “looks right.” Development procedures select them with nested walk-forward validation, parameter perturbation, multiple-testing records, complexity penalties and economic cost assumptions. Validation must include unseen periods and broker conditions. Evidence insufficient; requires testing.

## Participation modes

**Core:** persistent directional movement or continuation/pullback; lower turnover; one thesis per direction; invalidation and horizon mandatory. **Scalp:** local movement with short horizon; only where spread, latency and expected excursion support net economics; never silently duplicate core. **Micro-flow:** optional tick-level mode, disabled until feed and fill evidence support it; smallest allocation and strict attempt cap. All modes share symbol exposure and risk budgets.

## Entry, exit, re-entry

Entry creates an expiring intent with direction, mode, state, features, score, expected move, cost, stop, horizon, thesis ID and explanation. Preflight is repeated at send time. Breakout participation requires validated acceptance/retest unless immediate entry survives testing; pullback participation requires an intact parent direction and causal invalidation. Every position has a catastrophic protective stop, thesis invalidation, time/horizon exit, and optional target/trail only if tested. Stop widening and loss-recovery sizing are forbidden.

After exit, re-entry requires a new event sequence and renewed evidence. Cooldowns are mode- and reason-aware and become longer after stops, churn, slippage anomalies, repeated failures or abnormal conditions. An independent state transition can establish a new thesis but cannot bypass risk or execution controls.

## Adaptive frequency

Trade frequency is an output of opportunity arrival, confidence, net edge, cost, liquidity and available risk—not an objective. The controller can throttle or disable a mode when spread, latency, rejects, adverse selection, loss streaks or budget consumption deteriorate. It may permit high-frequency behaviour only when independent opportunities and execution results justify it. Risk per trade never increases merely because more opportunities arrive.

## Deterministic/statistical/ML separation

Deterministic components: event validation, formulas, causal structure, state safety precedence, hard risk limits, exposure, broker checks, stops, shutdown and logs. Statistical components: rolling distributions, calibration, uncertainty estimates, expected-move/cost estimates and parameter selection. ML components, if approved later, rank or calibrate opportunities under a frozen schema and fall back safely. None can override hard controls.

## Strategy test matrix

Test each movement class against no-trade and simple directional baselines; report net costs, state conditional outcomes, MAE/MFE, drawdown, turnover, exposure and uncertainty. Include failures: false breakout, trend chop, acceleration reversal, pullback invalidation, exhaustion continuation, spread shock, tick drought, latency, rejects, duplicate intents and restart. Retain only stable incremental evidence; never claim profitability.
