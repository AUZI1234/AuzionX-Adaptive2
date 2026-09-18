# Research Methodology

## Research status

This phase establishes measurement infrastructure only. No XAUUSD data is present in the repository, no measured market result is claimed, and no trading parameter is being optimized.

## Dataset partitions

- **Development data:** used to inspect distributions, define data-quality rules, design features, and predeclare analysis procedures. It may inform configuration selection, but every change is recorded.
- **Validation data:** the next chronological block, used once to evaluate frozen definitions and configuration. It must not be used to redesign the feature after inspection.
- **Out-of-sample data:** untouched until the research package is frozen. It is the final evidence block for generalization and may not be used for parameter selection.

Each partition includes warm-up data only from its own preceding history or an explicitly documented cold-start policy. Overlapping future labels require a time embargo between partitions.

## Reproducible workflow

1. Hash and manifest the raw data and broker metadata.
2. Validate without mutating raw files.
3. Create a deterministic normalized event stream and validation report.
4. Run causal feature generation; preserve invalid/warm-up flags.
5. Produce descriptive distributions by UTC session, volatility bucket and calendar period.
6. Create future outcome labels only in a separate table and never merge them into causal inputs.
7. Record observation, hypothesis, inference and measured result separately.
8. Report sample sizes, missingness, uncertainty and low-sample warnings.
9. Freeze code/schema/config hashes before validation and out-of-sample runs.

## No optimization rule

Phase 2 does not select profitable thresholds, score weights, risk values or entry rules. It measures tick flow, persistence, acceleration outcomes, excursions and costs. Any later selection requires chronological walk-forward validation, realistic spread/slippage/latency and a multiple-testing record.

## Required reporting

Reports must include dataset description, data quality, feature distributions, state frequencies, movement duration/excursion, spread and cost distributions, limitations, unresolved data dependencies and next experiments. Absence of data is a measured availability status, not permission to create synthetic conclusions.
