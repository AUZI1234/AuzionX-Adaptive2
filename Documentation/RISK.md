# AuzionX Adaptive v2 — Risk Blueprint

Risk is an independent veto and sizing authority. It evaluates signal risk, current exposure, pending reservations, account state, broker constraints and abnormal conditions before any order. A valid opportunity may be rejected.

## Controls

Define before implementation and select values through account/broker-specific stress analysis: per-trade and per-mode risk, aggregate open/contingent risk, gross and directional exposure, position/order count, daily loss, rolling drawdown, margin utilization, consecutive-loss and execution-failure locks, and frequency caps. Include spread, commission, slippage, gap and stop uncertainty. Size is the minimum of stop-risk budget, broker min/max/step, margin and exposure capacity. No martingale, averaging down or unapproved pyramiding.

## Hard vetoes and shutdown

Reject new risk for invalid/stale/crossed quotes, missing data, abnormal spread/volatility/gaps, unavailable risk state, unknown positions, invalid stop/freeze levels, insufficient margin, permission/session failure, duplicate intent, cooldown, daily/drawdown breach, or execution-health failure. A global lock blocks all new entries and follows the approved emergency position-management policy. Recovery requires sustained normal observations and reconciliation; one normal tick is insufficient.

## Position and failure handling

On startup/reconnect reconcile every broker position/order before signals. Unknown exposure locks trading. Netting accounts require explicit attribution; hedging accounts require group aggregation. Partial fills receive protective management immediately and re-enter risk evaluation. Rejected orders are classified and bounded; delayed acknowledgements are reconciled rather than retried blindly. Locks and counters persist through restart where possible, otherwise fail closed.

## Risk tests

Prove worst-case planned exposure, gap residual risk, stop protection, lock latency, restart persistence, duplicate prevention, netting/hedging semantics, repeated losses, spread explosion, missing ticks, broker rule changes, partial fills and disconnects. A risk reduction that lowers simulated return is not a defect. No profitability claim is made.
