# Source-day analysis technical protocol

## Outcome and unit
One observation per archive production day, ordered chronologically. A day is eligible only when its outcome date is present and all ten category counts are finite and nonnegative. The response is one when any count is positive; zero means no positive entry in the stored record, not independently inspected normality. Stored has_defect is used to check equivalence. The dimensional-reference category is excluded.

Before eligibility filtering, chronological production-day indices 1–115 define training, 116–147 validation, and the remaining indices test (the study design contains 51 test days before exclusions). Missing outcomes are excluded, not imputed. Same-calendar-day source association supplies daily context, not heat-specific inspection attribution.

## Reconstructed predictors
- H (3): source heat-record count; median and IQR of numeric positive recorded temperatures. Values at or below zero are excluded only from thermal summaries.
- HC (11): H plus arithmetic means of eight numbered OES channels, without assumed elemental identities or ratios.
- HCM (14): HC plus molding-record count, sum of nonmissing production quantities requiring at least one value, and distinct nonmissing source product count.
- HCMcal (17): HCM plus original day of month, weekday (Monday = 0), and month-end indicator.
- CAL (3): calendar fields alone.

An absent source group remains missing. No target-derived rejection, rework, monetary or final-defect fields are predictors. Source identifiers are used for aggregation or linkage, never as categorical predictors. Calendar fields are computed privately from original dates, not from public relative labels.

## Estimation and selection
Training-only median imputation with missing indicators precedes both estimators. LR additionally applies StandardScaler. LR uses C=1, L2, lbfgs, max_iter=5000, balanced class weights, random_state=42. RF uses 500 trees, min_samples_leaf=3, balanced_subsample, random_state=42 and n_jobs=2. Other options follow scikit-learn 1.6.1. Five input groups times two estimators give ten fits, with no hyperparameter search.

The validation threshold grid contains 181 ascending values from 0.05 to 0.95. Maximize balanced accuracy, then MCC, then F1, then choose the smallest threshold. Within an input group, select model family by validation BA, MCC, F1. Test outcomes are not used for selection.

Report all ten model results, validation choices, AUC, balanced accuracy, average precision, MCC, F1, confusion counts and flagged counts. The baseline assigns every test observation a positive prediction. Interpret paired source increments HC−H, HCM−HC, HCMcal−HCM and HCMcal−CAL.

## Fixed-model uncertainty
Use 2,000 paired test-day bootstrap samples and 2,000 circular five-observation block samples with random seed 42. Eligible observations after exclusions need not be consecutive calendar days. Omit resamples lacking both classes. These intervals hold fitted models and thresholds fixed; they do not include refitting or model-selection uncertainty.

## Limits
This is retrospective stored-record prediction, not a confirmatory physical-quality or operational deployment study. Public aggregates do not support independent model refitting. This protocol describes the supplied implementation and makes no new execution or reproducibility claim.
