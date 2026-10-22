# Running the main scheme

## Read and verify the completed results

Use `results/TABLE_INDEX.json` to locate tables. `main_full_metrics.csv` covers 105 domain-procedure combinations. Read CSV values with `float_precision='round_trip'`; pandas reads `.csv.gz` directly.

```text
python -m pip install -r requirements.txt
python analysis/verify_results.py
python analysis/verify_feature_exports.py
python analysis/verify_package.py
python analysis/reproduce_figures.py
```

These commands fit no estimators. Figure outputs go to `generated/figures/`; reference assets are not overwritten. Figure 1 is skipped unless authorized local coastline coordinates are supplied. All other main figures and seven regional diagnostic panels can be regenerated from the package. Set `HOTSPOT_COASTLINE_PATH` to a local NPZ containing `coast` line segments to regenerate the original map without changing its design; those coordinates are not distributed. `HOTSPOT_FIGURE_OUTPUT_ROOT` can select a separate figure-output directory.

## Run using the included processed inputs

1. Prepare the main modeling environment with `requirements-main.txt`. Original training versions are recorded separately; identical GPU retraining is not guaranteed.
2. Open `Hotspot_SameDay_Main.ipynb`. Leave `DATA_MODE='processed'`, the default. The notebook reads `data/processed/` and needs no original gridded downloads.
3. Run all cells with switches left at `False` to inspect definitions and the fit budget. No observations are read and no models are fitted.
4. Enable only `RUN_PREFLIGHT`, rerun Controls, and run the preflight cell. It validates CSV identity and calendars and creates a local cache. Save the printed `PREFLIGHT_DIR`.
5. Enable one scientific stage at a time: `RUN_MAIN`, `RUN_ABLATION`, `RUN_ROLLING`, `RUN_TEST`, then `RUN_REPORTS`. Disable the previous stage. Save `EXPERIMENT_DIR` and use the same configuration when resuming.
6. New results go to `outputs_main/`, separately from the manuscript evidence in `results/`.

The original full scheme requires 371 fits. Do not repeat training just to inspect saved results. The reporting stage can take substantial bootstrap time. For input-only validation without fitting, run `python analysis/verify_processed_inputs.py` in the main environment; it checks all seven domains and four schedules.

The processed tables retain the full SST context so every fitting prefix reconstructs its own monthly anomaly reference. Input meanings and known source qualifications are in `data/processed/README.md` and `docs/SOURCE_ATTRIBUTION.md`. The export does not alter the scientific input values or resolve upstream provenance gaps.

## Optional reconstruction from original grids

Set `DATA_MODE='raw'` and `DATA_PACKAGE_ROOT` to an authorized package containing the original `Data/`, 25 CMORPH annual files and `bundle_manifest.json`. This route retains the original aggregation code. Changing routes, files or source implementation requires a new preflight and experiment; do not mix artifact identities.

## Google Colab and storage

Place the repository in Drive and set `REPOSITORY_ROOT` to its Drive location. The startup cell mounts Drive when needed. The default processed route uses the included files; no separate raw-data package is required. Outputs persist only when `OUTPUT_ROOT` or the repository lies on Drive. Temporary `/content` storage does not persist.

## Optional diagnostics from original fitted models

`.local_paths.json` is private and excluded. On another computer, copy `local_paths.example.json` and set authorized original `experiment` and `preflight` locations. No fitted estimators are distributed. `python analysis/individual_feature/run.py --help` describes frozen perturbation inference, which can take time despite performing no fitting. Read the completed exports first. The main notebook cannot resume historical experiments with changed source identity.
