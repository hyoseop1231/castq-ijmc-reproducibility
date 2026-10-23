# Known reference differences

Documentation updated 2026-10-23. Differences are recorded per platform; no manuscript value was replaced.

## Linux aarch64 (earlier record, retained)

Four fresh model processes completed: three under Python 3.11.15 and one under Python 3.12.3 with the same pinned libraries, on Linux aarch64. All current reruns agree within the declared tolerances. The daily inputs, cohort, all ten point AUCs, balanced accuracies and confusion matrices agree with the supplied author results. The primary LR results agree.

On this platform the comparison with all supplied historical outputs did **not** pass. The following aggregate cells differ; some RF bootstrap interval/contrast limits also differ.

- HC RF threshold: reference 0.7499999999999999; current 0.7449999999999999.
- HC RF ap: reference 0.8013419784939838; current 0.8021555060516975.
- HCM RF ap: reference 0.7630733381972945; current 0.7633683169477512.
- HCMcal RF threshold: reference 0.5099999999999999; current 0.5149999999999999.

## macOS 26.2 arm64 (2026-10-23 rerun)

An independent Mac (macOS 26.2 arm64, Homebrew Python 3.11.14, Clang 17.0.0, numpy linked to Accelerate, OpenMP 20 threads) ran the private original analysis entrypoint with identical inputs, three SHA-matched input artifacts, and unmodified code and protocol. Three fresh processes with ten fits each completed.

- metrics.csv (10 rows), intervals.csv (20 rows) and contrasts.csv (16 rows) were byte-identical to the author original outputs in every run; nine files were compared directly by bytes.
- The daily table was byte-identical, and the cohort was 115/32/49.
- Repeated predictions differ by at most 2.220446049250313e-16; author predictions versus the macOS rerun differ by at most 7.993605777301127e-15.
- The RF threshold, AP and interval differences listed above did not appear on this platform.

The macOS machine is not an exact replica of the author's reported reference environment (macOS 26.3 arm64 Apple M4 Max, Homebrew Python 3.11.15, Clang 17.0.0, same packages, OpenMP 16 threads). Reproduction of the author aggregate outputs succeeded there even so.

## Unresolved

The Linux-platform RF threshold, AP and interval differences are not removed; they remain on record as platform-specific. The root cause is not established. Cross-platform and native-library effects are possible but unproven, and no arithmetic or threshold-selection rule was edited to force agreement. Individual scores and real day-level tables are intentionally not released.
