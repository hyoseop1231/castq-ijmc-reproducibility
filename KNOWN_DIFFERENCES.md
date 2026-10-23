# Known reference differences

Four fresh model processes completed: three under Python 3.11.15 and one under Python 3.12.3 with the same pinned libraries, on Linux aarch64. All current reruns agree within the declared tolerances. The daily inputs, cohort, all ten point AUCs, balanced accuracies and confusion matrices agree with the supplied author results. The primary LR results agree.

Full comparison with all supplied historical outputs did **not** pass. The following aggregate cells differ; some RF bootstrap interval/contrast limits also differ.

- HC RF threshold: reference 0.7499999999999999; current 0.7449999999999999.
- HC RF ap: reference 0.8013419784939838; current 0.8021555060516975.
- HCM RF ap: reference 0.7630733381972945; current 0.7633683169477512.
- HCMcal RF threshold: reference 0.5099999999999999; current 0.5149999999999999.

The source computation and thresholds were not edited to force the reference. The cause is unresolved. Cross-platform/native-library effects are possible but not established. Individual scores and real day-level tables are intentionally not released. Original manuscript values have not been silently replaced.
