# Naming and provenance

The active scheme's folder, notebook, module and functions use **main**. This replaces the former working name **lightweight** without changing the target, predictors, architectures, training weights, seeds, chronology, calibration rules, inversions or metrics.

The source notebook was `Hotspot_SameDay_Lightweight/Hotspot_SameDay_Lightweight.ipynb`. Its implementation was copied and identifiers were renamed consistently. Scientific-definition equivalence was checked through syntax-tree comparison after renaming, as recorded in `provenance/renaming_validation.json`. Startup paths are configurable, and new outputs use `outputs_main/`.

The new distribution identity differs from the historical source identity. Consequently, the main notebook must not resume historical experiment folders with a different source contract. Original experiment predictions and decisions remain the evidence for the manuscript results.

Original metadata in `provenance/recorded_run/`, dated reports and `COPY_MANIFEST.json` retain historical names and paths. Column names such as `hth_lag_0` are also retained to match exports and fitted models; the scientific term is dry-spell duration. These historical names do not indicate a separate active scheme or new data.

The copy manifest records source paths relative to the previous revision folder. Each copied result has source and destination SHA-256 hashes. For gzip files, the decompressed payload must match the original source hash. Packaging did not recompute results to replace CSV values.

Files under `reports/` are dated scientific records. Their statements about integration status describe the situation on their respective dates. The current release-folder status is documented by the repository README and release validation report.

## Option 2 input and packaging update

The 21 October 2026 processed-data update adds CSV dispatch to `RebuildConfig`, `source_inventory` and `load_region_daily_frames`, plus two CSV validation functions. The existing model, feature, calibration, inversion, scoring and reporting definitions remain unchanged. The notebook and module share the same definitions. Input route and file hashes enter fresh artifact contracts; original experiment folders must not be resumed across this change.

The initial copy manifest remains a historical record. Two explicit exceptions are now described in `provenance/CURRENT_TRANSFORMATIONS.json`: remove GADM `coast` coordinates from the plotting NPZ while verifying every retained array, and exclude the original Figure 1 PDF from the public payload. All saved prediction and metric values remain unchanged. Local backups preserve the removed assets.
