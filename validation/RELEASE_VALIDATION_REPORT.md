# Local repository finalization

22 October 2026. The package is prepared for its initial commit at https://github.com/raflialfansyah/climate-informed-hotspot-models. The repository exists, but this task does not commit, push, publish a release or change the manuscript and reviewer forms. The active scientific scheme remains the main same-day procedure with no optimized cross-model ensemble.

## Verification in this session

- All 105 main prediction series reproduce the 1,575 reported metric values, including MAE90 and RMSE90. Maximum absolute difference is 8.526512829121202e-14.
- All 364 individual-feature exports reproduce 29,484 feature means across five metric differences, totaling 147,420 checks. All 29,484 RMSE ranks match; maximum mean differences are zero.
- The included 63,917 region-date rows and 9,497 SST-context dates retain their original numeric hashes. All 28 region/schedule combinations reconstruct the expected 81 features and chronological support.
- The 20 code cells execute top to bottom with all scientific switches off. A second runtime copy executes with processed preflight only. No raw grids are loaded and no estimator fitting or model inference is performed. The distributed notebook remains unexecuted with all six switches off.
- The CFF 1.2.0 citation passes the official schema. Repository metadata are present; the author list now includes all six manuscript contributors, restoring Sri Nurdiati's omission from the initial candidate. No DOI, release date or journal acceptance is invented.
- The release validators check copied evidence hashes, gzip payload identities, Python/notebook syntax, complete manifest coverage, guide links, file sizes, ignored private/runtime files and bounded credential patterns. Current pass/fail evidence is in `package_checks.json`, `release_readiness.json`, `citation_checks.json` and the numerical check records.

The notebook checks use the existing local modeling environment with TensorFlow 2.20.0 CPU. No fresh Colab installation or repeat of the original 371 production fits is claimed. Existing figure assets and all scientific data/result files are protected by before/after hashes; figure regeneration from unchanged code is historical evidence below rather than a new run in this session.

## Source attribution and sharing

The confirmed original manuscript identifies NOAA OISST in Section 2.3.1, pages 8-9. The author supplied the ERA5 single-level CDS dataset URL on 22 October. Its catalogue is hourly; supplied files contain daily 00 UTC samples, without establishing a daily-mean wind value or evaporation accumulation interval. NASA/NOAA acknowledgements and Copernicus/ECMWF CC BY 4.0 attribution, dataset DOI and modification notices are included in `../docs/SOURCE_ATTRIBUTION.md`. MIT continues to apply to software and guides, separately from upstream data conditions.

The subsequently supplied MATLAB scripts establish OISST v2.1, the extraction regions and arithmetic spatial averaging. All 9,497 raw-context dates match the original regional CSVs exactly; all 14 historical derived columns reconstruct within 5e-12. See `../provenance/oisst/README.md`. The downloader omits 2000, and original-grid reconstruction and MAT-to-CSV export remain unshown. Dry-spell units/calendar correspondence, hotspot collection/sensor processing and ERA5 accumulation timing retain their separate qualifications. These are not described as entirely unknown product families. Source attribution does not independently authenticate historical download requests. Raw grids, fitted snapshots, private path configuration and GADM geometry/standalone map remain excluded.

## Release-file integrity

Git attributes disable newline conversion so a checkout preserves the exact bytes hashed by the release manifest. `verify_package.py` now checks manifest completeness and single-file limits, and does not mistake an ignored preflight cache for a distributed model/data file. Its report records the repository URL without claiming that no repository exists. The default validators never run training; the preflight validator changes only an in-memory runtime copy.

The manuscript, supplementary documents, all five reviewer forms and their trackers are outside the public payload. Their working files were protected during package finalization. Public access and the two reviewer availability comments must be verified after a later push. Normal author review of contributor attribution remains part of the publication checklist.

## Historical preparation records

The dated notes below describe the earlier local candidate. Their source-identity, SST-version uncertainty and repository-existence statements are superseded by the 22 October source review, author-script audit above and current source-attribution guide. Historical numerical-input manifests are retained unchanged; only current metadata explanations are corrected.

# Option 2 processed input update

21 October 2026. The local candidate now includes exact processed daily input CSVs, the full shared SST context, an input dictionary and a CSV-loading route in the main notebook. Existing saved predictions and results remain the manuscript evidence. This update did not repeat production fitting or model inference.

The package holds 63,917 domain-date records, seven domains with 9,131 dates each, plus 9,497 SST-context dates. CSV round-trip values and all reconstructed scientific feature values were compared exactly with the trusted original cache. All 28 domain-schedule combinations retained the same 81 features, chronological masks and training-derived high-day thresholds. The model, feature, calibration, inversion, scoring and reporting definitions remain unchanged; only the source configuration and dispatch interfaces changed, with two new CSV-validation helpers.

The main notebook ran top to bottom both with all switches off and with only processed preflight enabled. Original production fits were not repeated; future CPU/GPU retraining is not promised to be bitwise identical. Changed source identities require a fresh preflight and experiment. The untouched distribution notebook remains unexecuted with all scientific stages disabled by default.

All 105 main prediction series reproduce the 1,575 reported metric values, with maximum absolute difference 8.53e-14. Existing result files and retained figure assets keep their hashes. The coastline-free plotting NPZ preserves every non-coast array exactly. Eleven non-map main figures and seven regional diagnostics regenerate without local geometry. The optional original-map route was separately checked against the preserved local coastline. The original manuscript map is unchanged, while reusable GADM coordinates and the standalone map PDF are excluded from the public payload.

Source attribution distinguishes manuscript-reported MODIS Terra/Aqua via NASA FIRMS from unauthenticated original processing. The processed package retains the dry-spell calendar/unit, SST product and evaporation-interval qualifications. It is a local candidate, not a claim that every source-specific redistribution condition has been independently cleared. MIT applies to software and guides, not a newly assigned data license. No public repository or DOI has been created.

Evidence: `option2_validation.json`, `processed_input_checks.json`, `result_checks.json` and `package_checks.json`. The initial copy manifest is historical; `provenance/CURRENT_TRANSFORMATIONS.json` explains its two explicit GADM packaging exceptions. `provenance/RELEASE_MANIFEST.json` inventories the current public payload. Local paths, gridded source data, original preflight pickle, fitted models, generated figures and validation-runtime artifacts are excluded.


## Earlier preparation records

# Main scheme release-candidate validation

21 October 2026. Assessment: ready for local author review. MIT has been selected and applied to the software. Public release remains pending contributor-attribution review and documentation of redistribution terms for processed data and figure inputs. No GitHub repository, remote upload or DOI was created.

## Completed checks

- The renamed notebook has valid notebook structure. Its ten scientific definition cells are syntax-tree equivalent to the adopted source after consistent identifier renaming. Scientific model settings, features, chronology, calibration, inversions, seeds and metric formulas were preserved. Startup and output paths were made configurable.
- All 20 code cells executed top-to-bottom in the local verification environment with all six scientific stage switches off. No raw arrays were loaded and no estimator fitting was launched. The delivered notebook remains unexecuted and has all stage switches off.
- All 105 main procedure-domain prediction series cover the same 2,557 dates. Recalculation reproduced all 1,575 metric values, including MAE90 and RMSE90. Maximum absolute difference was 8.53e-14.
- All 364 individual-feature procedure exports contain 810 scores each. They cover 294,840 replicate scores and reproduce 29,484 feature means across all five reported metric differences, totaling 147,420 mean checks. The saved RMSE ranks were reproduced exactly using round-trip CSV reading.
- All copied result and provenance files were hash checked. Large CSV gzip payloads decompress to the exact original bytes. The historical metadata includes all 371 fitting records and seed-specific inversion decisions; executable model snapshots are excluded.
- All 12 main scientific figures and seven regional diagnostic panels regenerated from packaged inputs without estimator loading, inference or fitting. The latest three-metric Figure 7 bar layout was retained rather than the superseded heatmap. All 12 main figures retain the current PDF page geometry and extracted labels. Both contact sheets were visually inspected, including coastlines, IOD strips, zero labels, legends, negative R2 and the full feature-importance panel. Reference assets are copied without changes. Small raster differences in some regenerated figures arise from inherited plotting state/rendering details; pixel identity is not claimed for all regenerated assets.
- The main manuscript PDF, supplementary PDF and current Reviewer 1 DOCX retain their pre-task SHA-256 values. Original notebooks, saved result exports and models were not edited.
- No raw MAT/NetCDF files, model pickle/weights files, old ZIP archives, reviewer forms or manuscript sources were included. `.local_paths.json`, new experiment output, generated plots and runtime validation files are excluded by the prepared Git rules. A bounded scan found no configured GitHub-token, Google-key or private-key patterns in candidate text files. This is a packaging check, not a guarantee about every possible secret representation.

## Execution and reproduction boundaries

The full 371-fit production experiment was not repeated. The local verification environment uses TensorFlow 2.20.0 CPU; the historical production metadata records TensorFlow 2.21.0 with a visible GPU. Dependency lists record direct packages and are not a transitive environment lock. A fresh dependency installation and remote Colab execution were not performed during packaging.

The ported individual-feature runner was compiled and its CLI/input-location check passed for all 91 local main S5 bundles. Full frozen inference after the path/module port was not repeated. The previously completed 624 native-estimator replay cases and 3,120 metric checks are retained as historical evidence; these are not presented as a newly executed validation of the port. Use the configured original trusted snapshots and preflight cache for a full rerun, with outputs kept separate from manuscript results.

The figure runner covers the 12 main figures and seven domain panels. Two additional supplementary diagnostic assets and the TikZ workflow source are provided, but regenerating those two panels or compiling TikZ is not claimed by this runner.

Raw-product acquisition and all producer transformations are not reconstructed by the release. Dry-spell calendar/native-unit correspondence, the complete hotspot product lineage, SST product details and evaporation accumulation interval retain their documented qualifications. Data availability and redistribution rights are distinct from numerical agreement of the saved results.

## Evidence files

- `assembly.json` and `../provenance/renaming_validation.json`
- `notebook_execution.json` and `environment.json`
- `result_checks.json`
- `feature_export_checks.json`
- `package_checks.json`
- `figure_geometry_checks.json`
- `protected_working_files.json`
- `hygiene_checks.json`
- `../provenance/COPY_MANIFEST.json` and `../provenance/RELEASE_MANIFEST.json`

Runtime notebooks and rendered contact sheets remain local under ignored `runtime/`. Public-release decisions are listed in `../docs/PUBLICATION_CHECKLIST.md`.

## English documentation update

The repository README, running instructions, data availability notes, reproducibility guide, naming notes, publication checklist and nested guides are now in English. The two Indonesian guide filenames were replaced by `RUNNING.md` and `PUBLICATION_CHECKLIST.md`, and references were updated. The notebook's data-location Markdown cell was translated. Every notebook code cell, scientific source file, copied data asset and historical scientific report retains its previous content. This documentation-only update was checked for notebook structure, local links and unchanged protected-file hashes; production fitting and notebook execution were not repeated.

## MIT software license update

At the user's request, the provisional notice was replaced with the standard MIT License, the software citation now identifies MIT, and the README and release guides describe its scope. Scientific data, derived exports, figure assets and dated scientific reports are outside this software grant. All previously manifested files outside the six intentionally updated license/documentation files retain their hashes. The coastline array was checked directly and contains 14,301 two-endpoint longitude/latitude segments; its upstream dataset remains unidentified. No code, data values, figure assets or model settings were changed. Evidence is recorded in `mit_license_checks.json`.
