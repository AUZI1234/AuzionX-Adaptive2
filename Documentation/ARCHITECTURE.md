# AuzionX Adaptive v2 — Architecture Review

**Status:** implementation-ready blueprint; architecture review required before EA coding. **Instrument:** XAUUSD. **Decision:** BUY, SELL, or WAIT. **Claim:** none; evidence insufficient until testing is complete.

## 1. System boundaries and invariants

The system is a causal event-processing pipeline. Perception observes quotes; deterministic feature engines calculate measurements; state and opportunity engines infer conditions; risk and execution independently approve or veto; management handles existing exposure. No signal may bypass risk or execution. WAIT is the default. No module may increase risk to achieve a trade-frequency target. All timestamps, windows, parameters, data-quality flags, and decisions are versioned.

Every subsystem below specifies configurable parameters, but their values are not prescribed here. Values must be selected using development data, frozen, and evaluated on untouched data with realistic costs. A parameter is retained only when its incremental value is stable, economically meaningful, and not explained by leakage or multiple testing.

## 2. Interfaces and common objects

`TickEvent`: sequence, server/local timestamps, bid, ask, last, volume, flags, quote age. `FeatureSnapshot`: causal values plus sample counts, validity and source timestamps. `StateSnapshot`: state, confidence, quality, transition, age, evidence. `Opportunity`: direction, mode, score, expected movement, cost estimate, stop/exit plan, expiry, explanation, feature/model version. `RiskDecision`: approve/reject, size, reserved risk, veto codes. `ExecutionResult`: request/fill details, retcode, latency, slippage, partial status. `PositionRecord`: broker identifier, mode, thesis, entry, stop, expected horizon, MAE/MFE, exit reason.

## 3. Market Perception Engine

**Purpose:** create a trustworthy causal market event stream. **Inputs:** broker ticks, symbol specification, clock, trading-session metadata. **Outputs:** validated ticks, mid/microprice, spread, quote age, inter-arrival time, signed movement, tick-rate aggregates, multi-resolution bars, data-health flags.

**Calculations/rules:** reject nonpositive or crossed quotes; retain zero-change ticks with an explicit neutral policy; deduplicate by sequence/time/price policy; calculate mid `(bid+ask)/2`, spread in price and volatility units, returns only after a prior valid observation, tick rate, directional runs and quote gaps. Aggregate second/event bars without using future events. A stale, reversed, missing, or out-of-order stream produces `NO_DATA`/`ABNORMAL_MARKET` and blocks new entries.

**Dependencies:** broker feed, symbol precision, clock and volatility scale. **Failure:** stale quote, clock jump, invalid price, duplicate event, data drought, feed disconnect. **Config:** deduplication, maximum quote age, aggregation clocks, zero-tick policy, minimum samples, clock tolerance. **Tests:** replay ordering, duplicates, gaps, crossed quotes, restart, precision, clock changes, deterministic repeatability.

## 4. Market State Engine

**Purpose:** classify current behaviour without making state equal to a trade. **Inputs:** all feature snapshots, structure, flow, momentum, acceleration, volatility, execution health. **Outputs:** `NO_DATA`, `NO_TRADE`, `COMPRESSION`, `TREND_UP/DOWN`, `MOMENTUM_UP/DOWN`, `ACCELERATION_UP/DOWN`, `PULLBACK_UP/DOWN`, `BREAKOUT_CANDIDATE`, `BREAKOUT_ACCEPTED`, `EXHAUSTION`, `REVERSAL_RISK`, `ABNORMAL_MARKET`; confidence, quality, age and transition evidence.

**Rules:** score competing states, apply data-quality vetoes, persistence and hysteresis, minimum dwell time, and explicit transition evidence. A trend may become pullback when counter-movement occurs without structural invalidation; failed continuation becomes exhaustion/reversal risk. Abnormal/no-data always overrides. State labels are descriptive and cannot place orders.

**Dependencies:** perception, structure, flow, momentum, acceleration, volatility. **Failure:** insufficient samples, contradictory evidence, oscillation, stale state. **Config:** windows, minimum evidence, hysteresis, dwell/expiry, transition penalties and state precedence. **Tests:** every transition, oscillation suppression, missing data, abrupt gap, recovery, no-future-information replay.

## 5. Market Structure Engine

**Purpose:** represent causal short-term structure and movement context. **Inputs:** event bars, volatility scale, confirmed extrema. **Outputs:** swing sequence, range bounds, compression, displacement, pullback depth, breakout candidate/acceptance/rejection, invalidation levels, structure quality.

**Calculations/rules:** confirm an extremum only after the configured causal confirmation rule; calculate higher-high/lower-low sequences, net displacement versus path, range width and breakout distance normalized by volatility. A breakout requires post-event acceptance/retest evidence unless an immediate rule is separately validated. BOS/CHoCH/order-block terms are annotations, not mandatory setups.

**Dependencies:** perception and volatility. **Failure:** unstable swings, too few observations, gap through structure, ambiguous range. **Config:** aggregation resolutions, confirmation logic, lookback, acceptance duration, retest tolerance, invalidation policy. **Tests:** synthetic structures, boundary touches, gaps, repaint prevention, parameter perturbation.

## 6. Market Flow Engine

**Purpose:** measure local participation and directional pressure. **Inputs:** tick direction, volume/tick volume if reliable, bid/ask and optional book data. **Outputs:** signed tick imbalance, volume imbalance, buy/sell run lengths, flow persistence, absorption/rejection flags, flow quality.

**Calculations/rules:** define treatment of neutral ticks and unavailable volume; calculate rolling signed counts/volume and imbalance with sample-size quality. Book-derived measures are optional and must not be assumed representative of executed flow. Flow confirms or contradicts price movement; it does not independently guarantee direction.

**Dependencies:** perception, optional market depth. **Failure:** unreliable volume, feed-specific flags, sparse ticks. **Config:** windows, weighting, neutral policy, minimum samples, book timeout. **Tests:** synthetic flow, sparse volume, contradictory price/flow, feed changes, ablation.

## 7. Momentum Engine

**Purpose:** measure movement magnitude and directional consistency across horizons. **Inputs:** causal returns, volatility scale, structure, flow. **Outputs:** normalized signed returns, regression slope, impulse/range ratio, efficiency ratio, sign persistence, horizon agreement and quality.

**Rules:** use non-overlapping or explicitly labelled windows; normalize by contemporaneous, lagged volatility only; require minimum observations. Momentum is evidence for continuation only when costs and state are compatible.

**Dependencies:** perception, volatility, flow. **Failure:** near-zero scale, short sample, contradictory horizons. **Config:** horizons, normalization, winsorization, minimum sample. **Tests:** scale invariance, flat market, one-tick spike, leakage, horizon sensitivity.

## 8. Acceleration Engine

**Purpose:** detect changing velocity and distinguish strengthening from fading movement. **Inputs:** momentum series, elapsed time, volatility. **Outputs:** normalized velocity, causal acceleration/deceleration, acceleration persistence, impulse-quality change, confidence.

**Rules:** acceleration is the difference of previously available normalized velocities divided by elapsed time; winsorization and smoothing are causal and frozen before testing. Positive acceleration raises urgency and adverse-selection risk simultaneously; deceleration can reduce continuation confidence but does not automatically reverse.

**Dependencies:** momentum, volatility and clock. **Failure:** irregular timing, noisy derivative, missing history. **Config:** derivative horizon, smoothing, winsor limits, persistence, minimum sample. **Tests:** analytic ramps, impulses, irregular ticks, noise amplification, no future values.

## 9. Volatility Engine

**Purpose:** estimate movement scale and market-quality regime. **Inputs:** returns, ranges, spread and tick-rate history. **Outputs:** realized variance, robust dispersion, ATR-like range, volatility-of-volatility, percentile/regime, scale quality and abnormal flag.

**Rules:** use rolling causal estimators; retain sample counts; do not turn high volatility into a signal. Percentiles are calculated from a training/development history and validated out of sample. Spread is measured independently and jointly with volatility.

**Dependencies:** perception. **Failure:** zero/insufficient variance, gaps, regime discontinuity. **Config:** estimator, windows, percentile history, minimum sample, gap policy. **Tests:** constant price, jumps, heavy tails, estimator agreement, regime shift.

## 10. Opportunity Scoring Engine

**Purpose:** rank directional opportunities and decide whether a potential edge is executable. **Inputs:** state, structure, flow, momentum, acceleration, volatility, cost, execution health, risk capacity. **Outputs:** long score, short score, expected movement, conservative cost, uncertainty, expiry, BUY/SELL/WAIT intent and explanation.

**Rules:** maintain separate evidence ledgers. A direction requires sufficient data, compatible state, expected movement greater than spread+commission+slippage+adverse-excursion allowance, no hard contradiction, valid stop/size, risk approval, and preflight approval. If both directions conflict or margins are inadequate, WAIT. Scores and weights are not arbitrary: select via nested walk-forward development, sensitivity and complexity penalties; calibrate probabilities and report uncertainty.

**Dependencies:** all intelligence engines, risk and execution. **Failure:** missing feature, stale score, uncalibrated model, ambiguous direction. **Config:** weights, thresholds, expiry, uncertainty penalty, cost model, minimum edge and evidence count. **Tests:** decomposition, boundary conditions, cost shocks, tied directions, score reproducibility, ablation.

## 11. Core Position Engine

**Purpose:** participate in persistent directional movement with lower turnover. **Inputs:** accepted trend/continuation/pullback state, opportunity, risk allocation, existing thesis. **Outputs:** core intent, stop/invalidation, horizon and management policy.

**Rules:** one core thesis per direction unless a separately validated add-on creates new evidence and passes aggregate risk. Pullback participation requires preserved parent direction and causal invalidation. No averaging down or loss-recovery sizing. Core entries expire when state or execution quality changes.

**Dependencies:** scoring, structure, risk, execution. **Failure:** duplicate thesis, invalid stop, state contradiction, insufficient edge. **Config:** horizon, allocation, add-on policy, stop/target/trailing policy, intent expiry. **Tests:** trend, pullback failure, reversal, duplicate prevention, stop behaviour.

## 12. Scalp Engine

**Purpose:** shorter-horizon participation in validated local movement when economics support turnover. **Inputs:** short-horizon flow/momentum/acceleration, spread, latency, expected excursion, core exposure. **Outputs:** scalp intent and short expiry.

**Rules:** require a distinct horizon and positive net edge after actual cost distribution; do not duplicate a core thesis silently; reduce or disable under latency/spread deterioration. High activity is permitted only when opportunities and fills support it.

**Dependencies:** short-term features, execution and risk. **Failure:** cost dominates expected move, rapid churn, fill uncertainty. **Config:** horizon, cost multiplier, mode allocation, cooldown, maximum simultaneous scalps. **Tests:** cost sensitivity, latency, rapid reversals, thesis overlap, churn.

## 13. Micro-Flow Engine

**Purpose:** optional very-short-horizon flow participation. **Inputs:** high-quality tick stream, local imbalance, tick rate, spread, latency and fills. **Outputs:** minimal-risk micro intent or disabled status.

**Rules:** disabled by default until tick-level net evidence exists. Require stable feed, measurable imbalance, positive conservative edge and immediate exit feasibility. Never rescue losses, pyramid rapidly, or operate during abnormal conditions.

**Dependencies:** perception, flow, execution and risk. **Failure:** sparse/noisy feed, cost greater than movement, quote age, rejects. **Config:** enable flag, horizon, minimum sample, allocation, max attempts, cooldown and disable triggers. **Tests:** tick replay, adverse selection, spread shocks, delayed acknowledgements, disable/recovery.

## 14. Adaptive Risk Engine

**Purpose:** independently limit loss and disable new risk. **Inputs:** equity, balance, realized/unrealized P/L, stops, positions, margin, signal intent, execution health, daily/drawdown history. **Outputs:** veto/approval, size, reserved risk, locks and emergency action.

**Rules:** size from stop risk plus spread/commission/slippage/gap allowance, then cap by mode, direction, gross exposure, margin and broker volume. Daily loss, rolling drawdown, consecutive losses, execution failures and abnormal market conditions can lock entries. No martingale. Stops never widen.

**Dependencies:** account, exposure, execution and persistence. **Failure:** unknown position, stale counters, risk-service error, unprotected fill. **Config:** risk budgets, limits, lock/recovery policy, sizing model, margin buffer, consecutive-loss policy. **Tests:** worst-case loss, restart, partial fill, bypass attempts, boundary arithmetic, lock latency.

## 15. Exposure Manager

**Purpose:** aggregate all current and potential exposure across core/scalp/micro-flow. **Inputs:** broker positions/orders, reserved intents, stop distances, mode and thesis IDs. **Outputs:** net/gross exposure, directional concentration, available capacity and conflict decisions.

**Rules:** one symbol-level budget; netting accounts require attribution to net position, hedging accounts require group limits. Add, reverse, switch mode or stack only after recalculation. A scalp cannot hide behind core exposure.

**Dependencies:** broker reconciliation, risk and position records. **Failure:** unknown ticket, stale order state, duplicate intent, inconsistent account mode. **Config:** caps, correlation/thesis rules, reservation expiry, position limits. **Tests:** netting/hedging, pending orders, simultaneous intents, reconnect, partial fills.

## 16. Execution Engine

**Purpose:** translate an approved intent into a broker-valid, observable transaction. **Inputs:** intent, current quote, symbol/account constraints, filling mode. **Outputs:** request, result, fill/partial state, latency and slippage record.

**Rules:** preflight quote freshness, spread, permission, margin, volume step, stops/freeze levels, filling and deviation. Check every MQL5 return and trade-server retcode. Retry only bounded transient idempotent failures; delayed acknowledgement must reconcile, never duplicate. Missing protective stop is emergency state.

**Dependencies:** broker API, risk and symbol specification. **Failure:** reject, requote, partial fill, connection loss, invalid volume/stops, market closed. **Config:** deviation, retry policy, timeout, slippage tolerance, fill mode, stop policy. **Tests:** retcode matrix, delayed acknowledgement, partial fills, disconnect, reconciliation and emergency exit.

## 17. Trade Management Engine

**Purpose:** protect and close positions according to thesis, risk, state and execution. **Inputs:** positions, ticks, state, volatility, MAE/MFE, time and global locks. **Outputs:** modify/close intents, realized outcomes and reason codes.

**Rules:** every position has catastrophic stop, invalidation exit and time/horizon expiry. Optional targets/trailing/partial exits require evidence; stops may tighten but never widen. Reversal risk can close or reduce but cannot force a new reverse trade.

**Dependencies:** risk, execution, state and persistence. **Failure:** missing stop, rejected close, unknown position, stale management data. **Config:** stop/target/trail, time exits, emergency policy, partial rules. **Tests:** gap, fast move, reject, restart, stop modification, exit reason integrity.

## 18. Re-entry Engine

**Purpose:** prevent emotional/algorithmic churn while allowing genuinely new opportunities. **Inputs:** exit record, new event sequence, state transition, score, costs and risk locks. **Outputs:** re-entry allowed/blocked with reason and cooldown expiry.

**Rules:** an old intent cannot be reused. Stop losses, slippage anomalies, repeated same-direction failures and abnormal conditions lengthen cooldown; a validated independent structural transition may qualify a new thesis but never bypass risk. Re-entry must pass all normal gates.

**Dependencies:** management, state, frequency and risk. **Failure:** lost exit history, duplicate thesis, clock reset. **Config:** cooldown by mode/reason, event distance, independent-evidence rule. **Tests:** immediate signal repetition, new regime, restart, mixed modes.

## 19. Trade Frequency Controller

**Purpose:** adapt activity to opportunity supply and execution economics, never target a quota. **Inputs:** opportunity arrival, score quality, spread, volatility, latency, fill/reject/slippage history, losses and risk capacity. **Outputs:** permitted attempt rate, mode enablement, throttle or lock.

**Rules:** allow more decisions only when independent opportunities, costs and fills support them; throttle on churn, repeated loss, adverse selection, spread/latency deterioration, reject rate or budget use. Frequency limits are safety caps, not objectives. The controller cannot raise risk per trade.

**Dependencies:** risk, execution, state and all position engines. **Failure:** unavailable statistics or controller state; fail closed. **Config:** rolling windows, attempt caps, throttle levels, recovery observations, mode budgets. **Tests:** high-activity synthetic stream, cost deterioration, repeated failures, controller restart.

## 20. News/session/market-condition protection

**Purpose:** prevent unmodelled conditions from turning intelligence into uncontrolled execution. **Inputs:** session calendar, broker trading hours, optional trusted news/event feed, spread/volatility/tick-rate anomalies. **Outputs:** allowed/blocked state and reason.

**Rules:** no reliance on an unavailable news feed; if configured, event timestamps and revisions must be causal. Protect around configured high-impact events with research-validated blackout/reduced-risk policy. Session rules are broker-specific. Conditions such as gaps, spread explosion, tick drought, disconnection and extreme volatility override signals.

**Dependencies:** broker calendar, optional external data, perception and volatility. **Failure:** stale/missing calendar or news, timezone mismatch; choose explicit conservative fallback. **Config:** event sources, blackout/recovery windows, sessions, anomaly quantiles. **Tests:** timezone, revisions, feed loss, event shock, session boundaries.

## 21. Telemetry and decision logging

**Purpose:** make every action explainable and research-replayable. **Inputs:** snapshots, decisions, risk, execution, positions. **Outputs:** structured event records and health metrics.

**Required fields:** schema/version, code/parameter/model versions, event sequence/time, quote and spread, feature values/quality, state/transition/evidence, long/short scores and contributions, expected move/cost, decision and rejection/veto codes, risk/exposure snapshot, intent/thesis IDs, request/fill/retcode/latency/slippage, stop/exit reason, MAE/MFE and outcome. Log all rejected intents at a sampled/structured level; avoid unbounded normal tick logs. Persist enough for restart and audit.

**Failure:** write failure, clock mismatch, schema mismatch, sensitive data leakage. **Config:** sampling, retention, severity, persistence and redaction. **Tests:** schema validation, ordering, replay sufficiency, disk failure, volume bounds.

## 22. Backtesting architecture

Use an event-driven tick replay with bid/ask, broker contract, spread, commission, latency, slippage and fill/stop rules. The same causal feature code should be used in replay and eventual EA. At event time, only prior events are available; bar aggregation, swing confirmation, percentiles, labels and model features must enforce this. Split time chronologically into development, validation, untouched test and rolling walk-forward blocks. Never tune on the untouched block.

Compare no-trade, simple directional and deterministic adaptive baselines. Report net expectancy, uncertainty, MAE/MFE, drawdown magnitude/duration, loss streaks, exposure, turnover, cost fraction, fill/reject/slippage distributions, calibration and results by state/session/volatility. Stress costs, latency, gaps, spread, missing ticks, broker rules and parameter perturbations. A backtest cannot approve live trading.

## 23. Machine-learning research layer

ML is a challenger, not a safety component. Candidate targets are calibrated probability of net favourable excursion, adverse excursion, or state transition—not an unbounded BUY/SELL override. Features must be causal and versioned. Use time-series splits, embargo where labels overlap, calibration, drift/support checks, ablation, reproducibility and deterministic fallback. Compare against deterministic scoring and simple statistical models under identical costs. ML cannot override risk, exposure, execution, emergency or data-health controls.

## 24. Required implementation parameters

Data: quote age, aggregation clocks, zero-tick/dedup policy, sample minimums. Features: horizon sets, estimator windows, smoothing, winsorization, percentile histories. States: evidence, dwell, hysteresis, expiry and transition precedence. Scoring: weights, thresholds, uncertainty and cost model. Modes: horizon, allocation, stop/exit, overlap and cooldown. Risk: per-trade/mode/gross/directional/daily/drawdown/margin caps, loss/reject locks. Execution: deviation, timeout, retry, slippage and fill policy. Protection: sessions, event windows, anomaly quantiles and recovery. Telemetry: schema, sampling, retention. All require versioned validation records.

## 25. Acceptance gate

Do not create the final EA until all interfaces are reviewed, data semantics are frozen, deterministic replay exists, risk invariants pass adversarial tests, execution behaviour is demonstrated on the target broker, and untouched/walk-forward evidence is reproducible. No profitability statement is permitted.
