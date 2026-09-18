# Importing real XAUUSD tick data

The repository currently contains no real XAUUSD dataset. Synthetic fixtures are for software tests only and must never be used as market evidence.

## 1. Preserve raw data

Keep the vendor/broker export unchanged outside Git (for example `local_data/raw/xauusd_source.csv`). Do not place credentials, account data, or large proprietary files in the repository. Record its SHA-256 checksum in the manifest.

## 2. Convert to canonical CSV

Create a derived file with exactly these required columns:

```csv
timestamp_utc,bid,ask,sequence
2024-01-02T00:00:00.123Z,2040.10,2040.12,1
```

Convert the source timestamp using its documented timezone; never silently assume local time. Preserve source sequence when available. Calculate no derived prices in the import step. The canonical file may be stored outside Git, for example `local_data/canonical/xauusd_ticks.csv`.

## 3. Fill the manifest

Copy `dataset_manifest_template.json` to a dataset-specific manifest outside Git or into a reviewed small metadata commit. Fill broker/feed, contract metadata, coverage, source, format, checksum and limitations. Do not combine feeds without a documented normalization decision.

## 4. Validate without mutation

From the repository root:

```bash
python Research/data/validate_ticks.py local_data/canonical/xauusd_ticks.csv \
  --report local_data/reports/xauusd_validation.json \
  --gap-seconds 60
```

Use `--max-spread` only when the value is a documented data-quality rule, not a trading threshold. The command writes a report and never edits the input. A nonzero exit status means validation failed.

## 5. Generate causal features

Only after reviewing the validation report:

```bash
python Research/features/causal_features.py local_data/canonical/xauusd_ticks.csv \
  --output local_data/features/xauusd_causal_features.csv
```

The output is descriptive feature data; it creates no signals, orders, or trading parameters. Keep the original raw and canonical files unchanged.

## 6. Reproduce

Record the raw and canonical SHA-256 values, repository commit, Python version, command lines, manifest version and UTC run time. A failed validation must not be silently repaired; deterministic repairs require a new derived file and a new checksum.
