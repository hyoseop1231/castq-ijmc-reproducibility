# v0.1.0

- Received public-candidate analysis and reconstruction code preserved byte-for-byte. The analysis entrypoint differs from the original private execution file only by four input-filename substitutions.
- Added a technical PROTOCOL.md because the supplied public candidate required that missing file. Historical agent instructions and private provenance are excluded.
- Neutralized PDF Creator metadata; removed historical supplement-prose generation.
- Removed the individual-linkage diagram example; retained aggregate workflow diagrams.
- Published only three manuscript-level source-day aggregate CSV inputs; excluded private, monthly, rare-defect and per-record examples. Other optional plotting scripts require separately authorized aggregate inputs as documented.
- Added a fully synthetic schema/execution fixture, fixed core dependency lock, execution summary and explicit unresolved RF reference differences. No analysis arithmetic or threshold-selection rule was changed.

- The public technical protocol is a newly packaged document, not a claim of byte identity to the absent historical public protocol file. Its hash and this distinction are recorded in REPRODUCIBILITY.json.
- MIT license selected by the repository owner for the code; no industrial data release is implied.

# Documentation update 2026-10-23

- Documentation-only update to the existing v0.1.0 release; no new release, tag or publication was issued. No executable code, protocol or public aggregate CSV was modified.
- Added an independent macOS 26.2 arm64 rerun record: Homebrew Python 3.11.14, Clang 17.0.0, numpy 2.4.6 (Accelerate), pandas 3.0.5, scipy 1.17.1, scikit-learn 1.6.1, joblib 1.6.0, threadpoolctl 3.6.0, python-dateutil 2.9.0.post0, six 1.17.0, cloudpickle 3.1.2, OpenMP 20 threads, pinned in requirements-macos-reference.lock.
- Three fresh processes with ten fits each, using the private original analysis entrypoint and unchanged inputs, produced metrics.csv (10 rows), intervals.csv (20 rows) and contrasts.csv (16 rows) byte-identical to the author original outputs in every run (nine files compared directly). Daily table byte-identical; cohort 115/32/49.
- README, KNOWN_DIFFERENCES.md and REPRODUCIBILITY.json now record results per platform. The Linux aarch64 RF threshold, AP and interval differences are retained, not removed; their root cause is not established. Original manuscript values are unchanged.
- Replaced the earlier statement that macOS initialization never completed with the observed sequence: an initial local attempt failed, and a later run on a different, independently held Mac succeeded.
- Status changed from PARTIAL_REFERENCE_REPRODUCTION to COMPUTATIONAL_REFERENCE_REPRODUCTION_CONFIRMED_ON_MACOS. No claim of identical arithmetic across platforms, raw-data release or external-foundry validation is made.
