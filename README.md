# CASTQ IJMC reproducibility code

Research code and computational verification materials. See REPRODUCIBILITY.json and KNOWN_DIFFERENCES.md for the actual execution scope, successful checks and unresolved historical RF differences. Code is released under the MIT License. Industrial source data and private outputs are not included or licensed by this code release.

## Two different tasks
1. **Regenerate aggregate figures:** the three allowlisted figure_data files contain manuscript-level summaries, not private inputs or per-observation predictions. Plotting does not retrain models.
2. **Refit the source-day analysis:** requires separately authorized, nonpublic archive.csv and industrial SQLite inputs. They are intentionally absent. Aggregates alone cannot reproduce fitting. Historical comparison renderers require separately authorized aggregate inputs; this package does not supply their earlier training pipeline.

## Environment
The supplied build methods record Python 3.11.15, numpy 2.4.6, pandas 3.0.5, scipy 1.17.1 and scikit-learn 1.6.1. The pinned numeric libraries were executed on Linux aarch64 under Python 3.11.15 (three fresh processes) and Python 3.12.3 (one separate environment). macOS binary initialization did not complete; no macOS rerun success is claimed. requirements.lock records the tested core environment. The original matplotlib version is not established; the tested release renderer environment is pinned separately. Plotting is separately declared. The two supplied source-day aggregate figures were successfully rendered using the exact optional environment in requirements-plotting-tested.lock; this is not a claim of original-font or pixel-identical reconstruction.

### Default public aggregate regeneration (three CSVs only)

The public figure_data directory contains only source_day_metrics.csv, source_day_intervals.csv and source_day_contrasts.csv. Other original aggregate inputs are withheld; the additional renderers below are optional and require separately authorized inputs.

~~~sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-plotting-tested.lock
mkdir -p figures
python render_source_day.py
~~~

This renderer uses only the three public CSVs, writes source-day figure/contrast PDF, SVG and PNG outputs under figures/, and also writes current_results_table.tex. This command was executed successfully in the pinned release plotting environment; no pixel-identical original-font claim is made.

### Optional retained renderers, outside default public regeneration

The remaining rendering programs are retained as code, not a promise that every manuscript figure is reproducible from the three public CSVs.

- render_figures.py requires nonpublic additional aggregates associations.csv, importance_groups.csv, defect_profile.csv and monthly_profile.csv. Monthly and sparse-defect statistics are withheld pending explicit disclosure approval.
- render_daily_comparison.py requires nonpublic additional aggregates daily_metrics.csv and diagnostic_metrics.csv.
- render_integration.py requires nonpublic additional aggregate component_reproduction.json.
- render_method_diagrams.py is self-contained diagram code, with hardcoded study-level workflow descriptions rather than an extra CSV requirement. The unverified individual linkage illustration was removed; aggregate contextual integration and the F4 source-day workflow are retained. It is not part of the default three-CSV reproduction command.

The following commands are optional and are NOT the default public-data reproduction path. The first three require separately authorized private aggregate inputs at the expected package-relative paths:

~~~sh
python render_figures.py
python render_daily_comparison.py
python render_integration.py
# Separate retained schematic workflow, no external CSV input:
python render_method_diagrams.py
~~~

Historical supplement prose generation in render_source_day.py was omitted and PDF Creator metadata in render_figures.py was neutralized during earlier preparation. The current revision changes only the individual illustrative block in render_method_diagrams.py, not the fitting code.

## Private refit input schema
The following schema names describe required inputs, not supplied data. Keep all real dates and identifiers private.

- archive.csv: dissolution_date, defect_date, has_defect, and defect_ prefixed category columns: 사혼입, gh, 누탕, 파손, 크랙, 블로우, 수축, 중파손, 과절삭, 기타. All rows on a calendar day must agree on outcomes and outcome date.
- raw_db/process.db / tbDissolution: d_DL_Date, n_DL_Temperture.
- raw_db/process.db / tbModeling: d_ML_Date, n_ML_Count, n_ML_ITEM_ID.
- raw_db/observations.db / spectro_analysis_records: analysis_date, value_1 through value_8.

~~~sh
# Authorized private inputs only; use a fresh output directory:
python run_source_day.py --source-dir data --out outputs/source_day
~~~

run_source_day.py reads SQLite in read-only mode, requires adjacent PROTOCOL.md, and refuses an output directory already containing metrics.csv. This file is byte-identical to the supplied original public-candidate analysis file. Relative to the actual private execution version, four filename-reference lines differ; it is not claimed byte-identical to that private execution version. The final public entrypoint was executed against authorized private input snapshots in the separate Python environment. No private inputs or day-level outputs are included.

## Component reconstruction schema and commands
prepare_component_inputs.py additionally requires archive fields dissolution_id, dissolution_charge_no, dissolution_machine_id, dissolution_material_batch_id, dissolution_temp, dissolution_process_time, molding_qty_prod, molding_qty_reject; chemistry columns carbon_c, silicon_si, manganese_mn, phosphorus_p, sulfur_s, chromium_cr, nickel_ni, copper_cu. Source tbDissolution additionally requires n_DL_ID, n_DL_ChgNo, n_DL_MC_ID, n_DL_MTR_ID, s_DL_Time; tbModeling additionally requires n_ML_BadCount.

~~~sh
python prepare_component_inputs.py --source-dir data --out outputs/normalized
python reconstruct_components.py --inputs outputs/normalized --output outputs/component_summary.json
# Broader source relation audit, private inputs and private outputs only:
python reconstruct_source_relations.py --source-dir data --out outputs/relations
~~~

Normalized CSVs: archive_heats.csv uses archive_id,date,charge,equipment,material,temperature,time,production_count,rejection_count,F07–F14; source_heats.csv uses source_id,date,charge,equipment,material,temperature,time; spectro.csv uses date,F07–F14; molding.csv uses date,production_count,rejection_count. reconstruct_source_relations.py requires further original relational tables (including tbInjection, tbCheckFaulty, defect_records and their referenced source keys); its complete SQL/field contract is in the supplied script. These audits are separate from source-day fitting and must not be run using public aggregate files.

## Confidential outputs
PRIVATE_daily_table.csv, PRIVATE_predictions.csv, optional private crosswalks, all normalized inputs, source-integrity hashes, source-to-row mappings and the entire private reconstruction output directory must remain nonpublic. manifest.json contains source hashes, platform information and fit metadata and must not be uploaded unreviewed. Even files not named PRIVATE_ require disclosure review. .gitignore is a safeguard, not an authorization or anonymization mechanism.

## Public aggregate inputs and staging boundary

Final mandatory public data allowlist: figure_data/source_day_metrics.csv, figure_data/source_day_intervals.csv, figure_data/source_day_contrasts.csv, and no other data file. They are model/representation/bootstrap aggregate results, not individual dated observations or prediction lists. Inclusion does not certify non-reidentifiability or itself grant publication rights.

All other figure_data files are excluded from public staging, including monthly_profile.csv, defect_profile.csv, component_reproduction.json, daily_metrics.csv, diagnostic_metrics.csv, associations.csv and importance_groups.csv. They remain only in the preserved internal working candidate; do not copy the directory recursively. The single-linkage illustration remains excluded irrespective of pseudonym labels. Original preparation notes and pre-revision file snapshots remain in ignored tmp/ and must not be published. The parent will construct a new final-public folder using the exact metadata allowlist.

## Verification status

Four actual fresh-process runs completed. Current reruns agree with each other, and the primary manuscript LR results and all ten point AUCs/BA/confusion matrices match the author reference. Full historical-output comparison remains PARTIAL because some RF thresholds, AP values and bootstrap intervals differ. See KNOWN_DIFFERENCES.md. This is computational reexecution, not validation of casting-level defects or external-foundry transfer.

## Synthetic execution example

No industrial data are needed for this clearly synthetic smoke test. It demonstrates schema and execution only; it cannot reproduce the paper's reported performance.

~~~sh
mkdir -p outputs
python tests/make_synthetic_inputs.py --out outputs/synthetic-data
python run_source_day.py --source-dir outputs/synthetic-data --out outputs/synthetic-run
~~~

Private source data, dates, individual labels, individual scores and crosswalks must never be committed.

For the tested Linux plotting environment use `python -m pip install -r requirements-plotting-tested.lock`. The synthetic end-to-end smoke test and rendering of the two source-day figures completed successfully; synthetic performance is not the paper result.

## Version and licensing

Release: v0.1.0. Code license: MIT (LICENSE). No right to access or redistribute confidential industrial data is granted by this repository.
