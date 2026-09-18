# XAUUSD Tick Data Specification

## Scope

This specification defines the minimum causal input for Phase 2. No XAUUSD dataset is currently present in the repository; data availability is unresolved. The framework must report that condition rather than fabricate results.

## Canonical record

The canonical interchange format is UTF-8 CSV or Parquet with one row per quote event and these required fields:

- `timestamp_utc`: timezone-aware UTC timestamp with at least millisecond precision; nanosecond precision may be retained.
- `bid`: positive finite bid price.
- `ask`: positive finite ask price, `ask >= bid`.

Optional fields are `source_timestamp`, `sequence`, `last`, `volume`, `flags`, `source`, `symbol`, and `session_id`. `mid = (bid + ask) / 2` and `spread = ask - bid` are derived, never trusted as independent source values. Prices must retain decimal text or integer ticks before conversion when possible.

## Timestamp and ordering

Events are ordered by `(timestamp_utc, source_sequence)` when a trustworthy source sequence exists, otherwise by stable file order only after validation. Timestamps must not be silently localized. A timestamp collision is retained as separate events if quotes differ; exact duplicate rows are classified and excluded from derived movement calculations according to the configured duplicate policy. Out-of-order events are reported with counts and maximum displacement; strict mode rejects them, repair mode sorts only when the repair is explicitly recorded. No future event may be used to calculate a prior feature.

## Missing events and gaps

A missing tick cannot be inferred. The validator may identify an elapsed-time gap using a configured observation-duration threshold, but must not forward-fill prices or manufacture ticks. A quote gap is a price displacement between consecutive valid observations that exceeds a configured development-time anomaly rule; the rule is reported, not automatically deleted. Gap records remain available for stress tests.

## Zero-change ticks

A tick whose mid price equals the previous valid mid is retained. Its signed movement is `0`, its elapsed time is still observable, and it contributes to tick-rate/quote-count features but not directional movement counts. The neutral policy is versioned.

## Sessions and timezone

Storage and calculations use UTC. Session labels are derived from a versioned timezone/calendar configuration and never from local machine timezone. Session boundaries are metadata, not filters unless an experiment declares them. DST changes and broker server-time offsets are recorded in the manifest.

## Broker differences

Each dataset requires a manifest containing broker/feed, symbol name, digits, point, contract size, tick size/value if available, quote flags, volume semantics, server timezone, trading hours, spread policy, and collection method. Feeds can differ in aggregation, timestamp precision, missing bid/ask, volume meaning, and symbol suffix; datasets must not be silently combined.

## Validation rules

Validation reports row count, accepted/rejected rows, nulls, non-finite values, crossed quotes, nonpositive prices, ordering, duplicates, timestamp collisions, gaps, spread distribution, price precision, symbol metadata and source hash. Strict mode fails on required-field violations. Repair mode only performs documented deterministic transformations and writes a new version.

## Minimum history

No universal duration is asserted before observing the data. A study must predeclare the minimum event count and calendar coverage required for its feature/window/horizon and report insufficient samples. At minimum, development, validation and out-of-sample periods must be non-overlapping and each must contain the complete warm-up period for every tested feature.

## Storage and reproducibility

Raw source files are immutable and are not edited in place. Store large/private data outside Git and commit manifests, hashes, schemas, validation reports and small synthetic fixtures. Every run records dataset hash, code commit, schema version, timezone, configuration hash, Python version and UTC run time. CSV is the audit format; Parquet is an optional analytical format. No credentials or broker account data belong in Git.
