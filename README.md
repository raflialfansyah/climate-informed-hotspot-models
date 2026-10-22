# Main same-day hotspot estimation scheme for Indonesia

Companion package for [climate-informed-hotspot-models](https://github.com/raflialfansyah/climate-informed-hotspot-models), prepared on 21 October and verified locally on 22 October 2026. The main notebook is **[Hotspot_SameDay_Main.ipynb](Hotspot_SameDay_Main.ipynb)**. The active scheme and its functions use the name **main**. The scientific procedure is the scheme adopted for the manuscript revision.

## Getting started

1. Read the [running guide](docs/RUNNING.md).
2. Use the [table index](results/TABLE_INDEX.json) and `results/main/main_full_metrics.csv` for complete results across seven domains and 15 procedures, including MAE90 and RMSE90.
3. Read the [data availability and sharing status](docs/DATA_AVAILABILITY.md) and [reproducibility boundaries](docs/REPRODUCIBILITY.md).
4. Complete the [publication checklist](docs/PUBLICATION_CHECKLIST.md) before public release.

## Repository contents

| Location | Contents |
|---|---|
| `Hotspot_SameDay_Main.ipynb` | Standalone main notebook; all scientific execution switches are initially off |
| `src/main_scheme.py` | The same scientific definitions as the notebook, provided as a Python module |
| `analysis/` | Metric verification, figure regeneration and individual-feature diagnostics |
| `results/main/` | Predictions, complete metrics, calibration diagnostics, seed variation and intervals |
| `results/ablation/` | Matched predictor-group ablation |
| `results/temporal/` | Earlier temporal evaluation windows |
| `results/seasonal/` | Rainfall-defined dry/wet-stratum diagnostics |
| `results/individual_feature/` | Individual-feature analysis covering 2,557 dates, 10 repeats and four perturbation settings |
| `results/correlation/` | Bivariate correlations, with fitting-period and full-record results distinguished |
| `figures/` | Reference scientific figures; the GADM-containing Figure 1 is excluded from the public payload |
| `data/processed/` | Exact daily aggregate inputs and shared SST context; default notebook input route |
| `data/derived/` | Plotting inputs with GADM coordinate geometry removed |
| `provenance/` | Source identities, original configurations, inversion decisions and hash manifests |
| `reports/` | Dated scientific reports in English |
| `validation/` | Verification evidence for this release candidate |

Large CSV files use lossless `.csv.gz` compression. `src/release_io.py` reads both formats through the table index. Historical identities, feature names and result metadata are retained for traceability; see the [naming and provenance notes](docs/NAMING_AND_PROVENANCE.md).

## Scientific scope

The target is the satellite hotspot detection count on day t, an observation-based indicator of fire activity rather than a count of individual fires, burned area or severity. Environmental predictors extend through t, and observed hotspot history ends at t-1. Evaluation is retrospective on a period already examined during revision, with observed history supplied at each date.

- Fitting: 2001-2014; calibration: 2015-2016; inversion selection: 2017-2018; evaluation: 2019-2025.
- There are 81 features and 13 fitted procedures, plus Persistence and Monthly Climatology, across seven domains.
- For log-response models, a Duan factor is calculated from calibration residuals. Selection-period RMSE chooses plain or smeared inversion. Poisson and Tweedie predict counts directly.
- The original experiment used 203 main, 84 additional ablation and 84 temporal fits, totaling 371. Verification of saved results requires no additional fitting.
- Individual-feature importance is a later diagnostic without refitting. It is distinct from the retrained predictor-group ablation.

The main scheme uses no Lasso feature selection or optimized combination across model classes. All prespecified seeds are retained. See the [scientific protocol](docs/SCIENTIFIC_PROTOCOL.md) for details.

## Quick verification without raw data

Run these commands from this folder:

```text
python -m pip install -r requirements.txt
python analysis/verify_results.py
python analysis/verify_feature_exports.py
python analysis/verify_package.py
```

The main notebook defaults to the included processed inputs (`DATA_MODE='processed'`). Use `requirements-main.txt` for model-related work and `python analysis/verify_processed_inputs.py` for zero-fit input reconstruction checks. The recorded original training environment is listed separately in `requirements-recorded-run.txt`.

## Release status

The notebook, Python code and accompanying software guides are licensed under the [MIT License](LICENSE). See [license scope](docs/LICENSING.md) for data, scientific reports and figure exclusions.

Raw data and fitted model snapshots are excluded; `.local_paths.json` connects local artifacts and is excluded from Git. The manuscript, reviewer forms, revision archives and previous ZIP files are also excluded. The coastline source is author-identified as GADM, with Cartopy and a 5 km boundary buffer; see the [coastline source note](provenance/COASTLINE_SOURCE.md). GADM permits academic article maps, but data redistribution requires prior permission under its published terms. GADM coordinate geometry and the standalone original map PDF are excluded from the public payload. Processed aggregate inputs are included with NASA/NOAA source attribution and the applicable Copernicus/ECMWF CC BY 4.0 notice. The original manuscript and [author-supplied MATLAB scripts](provenance/oisst/README.md) document OISST v2.1 and regional index construction; the author identifies ERA5 single levels as the wind/evaporation source. Remaining scientific metadata qualifications are listed in [source attribution](docs/SOURCE_ATTRIBUTION.md). MIT for the code does not relicense data or third-party assets.


## Processed input package

Option 2 includes 63,917 domain-date input rows and 9,497 shared SST-context dates, with a data dictionary and SHA-256 manifest. CSV reconstruction preserves the original numerical inputs; all 81 feature definitions and the fitting/calibration/selection rules remain unchanged. See [processed inputs](data/processed/README.md). Saved predictions and scientific results are retained without replacement. Numerical verification and source attribution are documented in [the release validation report](validation/RELEASE_VALIDATION_REPORT.md). Version and citation metadata are in [CITATION.cff](CITATION.cff).
