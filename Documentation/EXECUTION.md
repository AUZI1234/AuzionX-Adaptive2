# AuzionX Adaptive v2 — Execution Blueprint

## Preflight and fill contract

Immediately before sending, validate symbol/account permission, quote sequence and age, bid/ask, spread in price and volatility units/percentile, state protection, volume min/max/step, margin, stops/freeze levels, filling mode, session, deviation, intent expiry, thesis duplication and risk reservation. Recompute net expected edge from the current quote.

Record decision quote, request quote, fill quote, times and latency, requested/filled volume, spread, commission, slippage, retcode, broker comment, partial status and order/position identifiers. Separate spread, commission, positive/negative slippage and exit costs. Slippage/deviation policies are broker/session/volatility distributions selected on development data and verified out of sample, not universal point constants.

## Errors and protection

Check all MQL5 return values and trade-server retcodes. Handle invalid volume/stops, requote, market closed, no money, connection failure, disabled trading and partial fill distinctly. Retry only bounded transient idempotent failures. An unacknowledged request is reconciled by broker identifiers; it is never duplicated. A position without a protective stop enters emergency handling. If execution or quote quality fails, new entries stop.

## Testing

Use a retcode matrix, simulated latency, spread shock, gap, stop/freeze changes, rejected/partial orders, duplicate callbacks, reconnect and restart. Compare assumed and realized costs. No compilation result is evidence of execution safety or profitability.
