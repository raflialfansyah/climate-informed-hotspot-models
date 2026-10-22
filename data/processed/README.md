# Processed daily model inputs

This package contains exact exports from the adopted main experiment's daily preflight cache. It supplies 63,917 domain-date records: seven domains, each with 9,131 daily dates from 1 January 2001 to 31 December 2025. The separate shared SST context retains 9,497 dates from 1 January 2000 to 31 December 2025. No source grids, fitted models or coastline coordinates are included here.

| File | Contents |
|---|---|
| `regional_daily_inputs.csv.gz` | Domain, date and eleven unstandardized numerical input/target columns |
| `sst_context.csv.gz` | Date and three supplied SST series, including the pre-2001 context used by fitting-prefix monthly references |
| `processed_input_manifest.json` | Schemas, dates, SHA-256 hashes, original numerical digests, fixed-support metadata and source qualifications |
| `DATA_DICTIONARY.csv` | Column definitions, units and interpretation limits |

CSV values use 17 significant digits. Read with pandas `float_precision='round_trip'`; the notebook's loader does this automatically and restores float64 numeric columns. Dates are ISO calendar dates. The input route validates hashes, complete ordered unique dates, domain coverage, finite values and agreement of the shared climate inputs. No missing-data filling, date shifting or value correction was introduced during export.

`issue_date` is a retained internal name for the target-day calendar; it is not an authenticated operational issue time. `hth_mean_issue` is the retained code name for regional mean dry-spell duration, not an integer regional days-since-rain counter. Evaporation stays signed in millimetres of accumulated depth, without assuming a verified daily accumulation interval. The stored dry-spell calendar correspondence remains qualified in the original manifest. The later source review and author-supplied scripts identify NOAA OISST v2.1, Celsius, the Niño 3.4 and IOD regions and arithmetic spatial averaging, with raw columns exactly matching this context. The original 21 October manifest retains historical source qualifications, superseded for SST by `../../provenance/oisst/README.md`; its numerical hashes remain valid. ERA5 accumulation timing retains its separate qualification. See `../../docs/SOURCE_ATTRIBUTION.md`.

The main notebook defaults to `DATA_MODE='processed'`. Enable only `RUN_PREFLIGHT` first. This constructs a new local cache without raw MAT/NetCDF input. For later training, use a fresh experiment: packaged aggregate inputs do not authorize resuming the old experiment with a changed source identity. All fitting switches remain off by default.

Features are reconstructed by the unchanged scientific functions. The 81-feature dictionary is `../../results/main/Supplement_S1_81_features.csv`; groups are S2=26, S3=59, S4=54 and S5=81 columns. Each fitting prefix recomputes its own SST monthly reference from the shared context. A fixed full-record anomaly table must not replace that step. The common 60-day warm-up leaves 9,071 modeled rows per domain, with 5,053 main fitting rows and 2,557 main scoring rows.

Verify the portable inputs with `python analysis/verify_processed_inputs.py` from the repository root in the main modeling environment. This reconstructs all 28 domain-schedule combinations and performs zero fitting and inference. Saved predictions and results remain in `../../results/` and are not replaced by this export.

Source attribution and data sharing are separate from the MIT software license. See `../../docs/SOURCE_ATTRIBUTION.md` and `../../docs/LICENSING.md`. This is a local release candidate; source notices, licence conditions and historical metadata qualifications remain documented, and no public upload has occurred.
