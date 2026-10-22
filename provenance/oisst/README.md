# OISST source and regional-index construction

Author-supplied scripts received on 22 October 2026 establish OISST v2.1 (`v02r01`) and the regional construction below. The two MATLAB files in this folder are unchanged provenance copies. Their SHA-256 identities and numerical checks are recorded in `../OISST_SOURCE_AUDIT_2026-10-22.json`.

| Item | Executable evidence |
|---|---|
| Download product | `GeT_DaTa_OISST.m`, lines 4 and 20: NOAA NCEI `/v2.1/access/avhrr/YYYYMM/oisst-avhrr-v02r01.YYYYMMDD.nc` |
| Download loop | `GeT_DaTa_OISST.m`, line 10: daily files for 2001-2025 |
| Niño 3.4 box | `Proses_data_Nino_IOD.m`, line 32: 190 < longitude < 240 degrees east and -5 < latitude < 5 degrees north, equivalent to 170-120 degrees west and 5 degrees south to 5 degrees north |
| Western IOD pole | `Proses_data_Nino_IOD.m`, line 97: 50 < longitude < 70 degrees east and -10 < latitude < 10 degrees north |
| Eastern IOD pole | `Proses_data_Nino_IOD.m`, line 103: 90 < longitude < 110 degrees east and -10 < latitude < 0 degrees north |
| Spatial means | Lines 34 and 99: arithmetic means over selected grid cells, without latitude weights; Niño uses `mean(...,'all')`, while IOD poles omit missing cells |
| Historical indices | Line 45 onward: monthly climatologies pool daily values over 2000-2025; daily anomalies subtract their calendar-month mean; line 126: IOD is western minus eastern anomaly |

The [NOAA product description](https://www.ncei.noaa.gov/products/optimum-interpolation-sst) documents daily 0.25-degree OISST. A [NOAA v02r01 sample header](https://www.ncei.noaa.gov/thredds/dodsC/OisstBase/NetCDF/V2.1/AVHRR/202006/oisst-avhrr-v02r01.20200601.nc.html) identifies `sst` in Celsius with scale factor 0.01. The scripts read `sst`, rather than NOAA's `anom` variable. MATLAB [`ncread`](https://www.mathworks.com/help/matlab/ref/ncread.html) applies file scale/offset attributes; no additional manual scaling is shown or needed for that interface. This documents the intended units, not inspection of every historical source file.

## Relationship to the adopted main scheme

The three original raw regional columns match every packaged SST-context value exactly on all 9,497 dates from 2000 through 2025. Reconstructing all 14 historical climatology/anomaly columns from those CSVs agrees within 1.17e-13, consistent with decimal export rounding. This supports the supplied transformation description; it does not replace a rerun from the gridded SST files.

The main scheme's `src/main_scheme.py`, `_load_climate_csvs` and `prepare_fit`, reads only `data_nino`, `data_pole_barat` and `data_pole_timur`. It ignores the supplied full-record anomalies and monthly indices, then freezes a monthly reference using SST dates through each fitting cutoff. The main reference uses the retained 2000-2014 context; subsequent calibration, selection and evaluation dates do not enter that reference. No input, anomaly definition, feature, fit, prediction or metric is changed by this source clarification.

The processing script expects 2000-2025 files, whereas the download script begins in 2001. The complete 2000-2025 CSV context is present; acquisition of the 2000 source files is not shown in these scripts. The MATLAB scripts save MAT tables; the MAT-to-CSV export command was not supplied. Original gridded files and MATLAB execution were not reconstructed during this audit. These limited provenance gaps do not require discarding the documented version, regions or averaging method.
