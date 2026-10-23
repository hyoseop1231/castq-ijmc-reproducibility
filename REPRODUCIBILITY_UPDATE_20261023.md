# Reproducibility update, 2026-10-23

Documentation-only update to the existing public code release v0.1.0. No code, protocol or public aggregate CSV changed; no new release was published.

## What was run

An independently held Mac (macOS 26.2 arm64, Homebrew Python 3.11.14, Clang 17.0.0, numpy linked to Accelerate, OpenMP 20 threads) executed the private original analysis entrypoint against identical inputs, confirmed by three matching input SHA-256 values. Code and protocol were unmodified. Three fresh processes with ten fits each completed. Package versions are pinned in requirements-macos-reference.lock.

## Result

- metrics.csv (10 rows), intervals.csv (20 rows) and contrasts.csv (16 rows) were byte-identical to the author original outputs in every run; nine files were compared directly by bytes.
- The daily table was byte-identical. Cohort sizes were 115/32/49.
- Maximum prediction difference between repeated runs: 2.220446049250313e-16. Maximum difference between author predictions and the macOS rerun: 7.993605777301127e-15.

## Relation to the author reference environment

The author's reported reference environment is macOS 26.3 arm64 on Apple M4 Max, Homebrew Python 3.11.15, Clang 17.0.0, the same package versions, and OpenMP 16 threads. The rerun machine is not an exact replica (different OS build, Python patch version, CPU and OpenMP thread count), yet numeric reproduction of the aggregate outputs succeeded.

## Platform status

- Linux aarch64: the four earlier fresh-process runs (three on Python 3.11.15, one on 3.12.3) are retained. Some RF thresholds, AP values and bootstrap intervals differ from the author reference there.
- macOS 26.2 arm64: the aggregate outputs matched byte-for-byte and no such RF differences appeared.

The Linux differences are not resolved and are not restated as fixed; they remain on record as platform-specific. The root cause is not established.

## Scope limits

This is computational reexecution of aggregate outputs. It is not a claim that all platforms produce identical arithmetic, not a raw-data release, not an individual-level disclosure, and not validation of casting-level defects or external-foundry transfer. Original manuscript values are unchanged. Status: COMPUTATIONAL_REFERENCE_REPRODUCTION_CONFIRMED_ON_MACOS.

## Prior attempt

An earlier macOS attempt on the initial local machine stalled before fitting completed; no security settings were changed. A later run on a different, independently held Mac produced the result above.
