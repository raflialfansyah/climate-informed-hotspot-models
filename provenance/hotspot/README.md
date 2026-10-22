# Hotspot daily extraction provenance

The author supplied `A1_Ekstraksi_Harian.m` on 22 October 2026. The public copy preserves the extraction calculations. Only the optional coastline display block was adapted: a personal absolute folder path was replaced with a relative `local_coastlines` folder, guarded so that missing outlines do not stop the script before saving. No coastline files or raw hotspot records are distributed. Original and public SHA-256 identities are in `../HOTSPOT_SOURCE_AUDIT_2026-10-22.json`.

## Documented processing

| Step | Executable evidence |
|---|---|
| Input | `readtable('fire_archive_M-C61_721000.csv')`; the filename includes M-C61, without independently authenticating file contents or metadata |
| Quality/type | Remove rows with `confidence<=80`, then retain `type==0`. For finite confidence this implements the stated >80 cutoff. The script does not add a separate missing-confidence check. |
| Day assignment | Convert `acq_date` to datetime if needed, then use `dateshift(...,'start','day')`. `acq_time` is not read and no timezone conversion is applied. |
| Grid | 0.25-degree edges from -11 to 6.25 latitude and 95 to 141.25 longitude. This yields 69 x 185 cells; centers span -10.875 to 6.125 and 95.125 to 141.125 degrees. Coordinates outside the configured edges are discarded by `discretize`. |
| Calendar | Complete daily vector from 1 January 2001 to 31 December 2025, 9,131 dates. Records outside this calendar are excluded with `ismember`. |
| Counts | `accumarray` adds one for each retained record to a latitude-longitude-day cube and fills empty bins with zero. There is no explicit deduplication or sensor-based adjustment. |
| Outputs | Save `X`, `lon_centers`, `lat_centers` and `days` to `hotspot_daily.mat`. No cell-activity threshold is applied here. |

The local supplied MAT has the expected 69 x 185 x 9,131 cube and exactly matching spatial centers. The raw CSV was not supplied with this script, so extraction was not rerun in MATLAB and point-to-cube numerical identity has not been established. The main package's seven aggregate series and all fitted results remain unchanged.

The complete calendar and zero fill are a representation of retained detections. They do not establish continuous satellite observation coverage or verified absence of fire. Multiple detections of a continuing fire, or repeated input rows, remain separate counts. Terra/Aqua continuity, original record-level metadata and timezone conventions remain qualifications; grid-resolution and boundary sensitivity have not been tested.

## Optional local execution

Place the authorized FIRMS CSV with the expected name in the MATLAB working directory and run the script in MATLAB with sufficient memory for the dense cube. Saving writes `hotspot_daily.mat` in that working directory. For the optional map outlines, place authorized `borderindonesia.mat` and `bordertetangga.mat` files in `local_coastlines/` beside the script. They are not needed for extraction or saving. This historical script is a provenance companion; the main Python notebook defaults to the packaged processed aggregate inputs.
