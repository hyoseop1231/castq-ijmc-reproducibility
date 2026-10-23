# Explicitly synthetic execution-smoke fixture

`make_synthetic_inputs.py` uses only the Python standard library and accepts no
source-data path. It does not read author data, industrial databases or the
manuscript's data. It performs no network operation. All records are deliberately
simulated; this is a schema/execution smoke fixture, **not reproduction of author
data, manuscript metrics, scientific findings, or physical process behaviour**.

## Generate a fresh fixture

From the package root, choose an existing, trusted parent and a NEW directory:

```sh
python3 tests/make_synthetic_inputs.py --out synthetic_smoke_inputs
```

The required `--out` must not already exist, even if empty. Symlink targets and
symlink ancestors are rejected. Its parent must already exist. Directory/file
creation is exclusive; partial output is retained on failure rather than deleted.
Use a trusted parent: the simple path checks are not race-proof against a hostile
concurrent process replacing directory components. Choose a different new output
path for each retry. No existing input or output is overwritten or removed.

Generated files:

- `archive.csv`: `dissolution_date`, `defect_date`, `has_defect`, and ten columns
  `defect_사혼입`, `defect_gh`, `defect_누탕`, `defect_파손`, `defect_크랙`,
  `defect_블로우`, `defect_수축`, `defect_중파손`, `defect_과절삭`, `defect_기타`.
- `raw_db/process.db`: `tbDissolution(d_DL_Date, n_DL_Temperture)` and
  `tbModeling(d_ML_Date, n_ML_Count, n_ML_ITEM_ID)`.
- `raw_db/observations.db`:
  `spectro_analysis_records(analysis_date, value_1, ..., value_8)`.
- `SYNTHETIC_FIXTURE.txt`: explicit simulation provenance, not source provenance.

There are 198 consecutive **simulated** dates beginning 2000-01-01. These are not
real observation dates. The seed is fixed at 20261023. Exactly one archive row per
simulated day guarantees day-level outcome consistency. Arbitrary alternating
labels supply both classes in training, validation and test. Nonnegative category
counts agree with `has_defect`; only the last two test days have missing outcome
dates. The source-day chronological design therefore has eligible split sizes
115/32/49 (before exclusions: 115/32/51). Heat/molding/OES record counts and values
are seeded random draws with no claim to realistic distributions or causal
relationships. Reproducibility means deterministic generation under the same
Python implementation, not stable SQLite byte hashes across versions.

## Optional later pipeline smoke run

After creating a fixture, and only in a separately prepared analysis environment:

```sh
python3 run_source_day.py --source-dir synthetic_smoke_inputs --out outputs/synthetic_smoke
```

This is documentation for a later smoke run, **not a claim that it was run or
passed**. The generator does not install dependencies, import the analysis code,
train models, or invoke this command. A fresh output path is recommended; the
analysis program's existing-output checks still apply. No metrics should be
compared with paper results, interpreted as scientific validation, or merged with
reported manuscript aggregates. This fixture targets `run_source_day.py` only,
not the broader component/relation reconstruction programs.

Analysis-created `PRIVATE_*` files remain per-simulated-observation outputs. Keep
all generated fixture databases, outputs, manifests and predictions outside the
public staging allowlist; publish the generator and this explanation only when
separately approved. Preparation here is limited to static AST syntax checking;
actual fixture generation and pipeline execution are separate checks.
