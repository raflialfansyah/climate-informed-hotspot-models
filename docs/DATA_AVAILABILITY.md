# Data availability and sharing status

This inventory distinguishes locally available files from permission to distribute them publicly. Local availability is not evidence of redistribution permission. No original gridded raw-data files were copied into this candidate, and nothing has been uploaded publicly. Option 2 now includes exact processed daily input exports and the saved scientific outputs.

| Category | Available in this candidate | Packaging decision |
|---|---|---|
| Notebook and analysis code | Included | MIT License selected and applied on 21 October 2026; see `../LICENSE` and `LICENSING.md` |
| Metrics, predictions and diagnostic tables | Included as candidate derived data | Study-generated outputs supplied for reproducibility; underlying source notices and licence conditions are retained in `SOURCE_ATTRIBUTION.md` |
| Processed model inputs | `data/processed/` | Included as a local candidate: daily aggregates, full SST context, definitions, source qualifications and hashes; NASA/NOAA and Copernicus source notices are provided; remaining historical metadata qualifications are documented |
| Derived figure inputs | `data/derived/figure_inputs.npz` | Aggregate counts, grids, masks and phase flags are retained; GADM coastline coordinates have been removed |
| GADM coastline and original map PDF | Excluded from the public payload | Recoverable from the local before-edit archive; optional authorized geometry can be supplied locally for Figure 1 |
| Hotspot MAT data | Excluded | Sensor composition, acquisition and producer filtering are not fully authenticated from the supplied cube |
| Annual CMORPH ADJ files | Excluded | Local files cover 2001-2025 on a 0.25-degree grid in mm/day; identities are recorded in the inventory |
| Dry-spell MAT and CRT source data | Excluded | The generator uses CMORPH CRT and an inclusive <=1 threshold in native units; calendar correspondence and source units retain qualifications |
| Evaporation and wind NetCDF data | Excluded | Author identifies ERA5 single levels through CDS; CC BY 4.0 attribution is included; the evaporation accumulation interval remains unconfirmed |
| Original SST and climate-index CSV inputs | Excluded; exact raw SST columns are included in `data/processed/` | Author scripts identify OISST v2.1, Celsius, Niño 3.4 and IOD boxes and unweighted means; script copies and checks are included in `provenance/oisst/` |
| Fitted models and preflight cache | Excluded | Available at local locations configured in `.local_paths.json`; not required to read or verify saved metrics |
| Manuscript, reviewer forms, ZIP files and internal archives | Excluded | Outside the scope of this code-and-results release |

## Optional raw inputs for reconstruction

The default notebook route uses the included `data/processed/` CSVs. For `DATA_MODE='raw'` only, use this original package structure:

```text
data_package/
  bundle_manifest.json
  Data/
    hotspot_daily.mat
    hth_daily.mat
    Evaporation.nc
    Wind_UV.nc
    MJO.csv
    dataIod.csv
    dataNino.csv
  cmorph_v1_adj_025deg_indonesia_v1/
    annual/    (25 annual files for 2001-2025)
```

The internal filename `hth_daily.mat` is retained for compatibility; the scientific variable is dry-spell duration. The author-supplied MATLAB code interpolates CRT rainfall to the hotspot grid, marks values <=1 as dry, and updates a consecutive-day counter. NaN values reset the counter because the comparison returns false; missing files are skipped. The script does not save a date vector. Its 2001-2025 loop produces at most 9,131 steps, whereas the supplied MAT contains 9,497; the loader assumes a 2000 start and then retains dates from 2001. This is an unresolved calendar-correspondence qualification, not proof of incorrect dating. Do not silently shift dates or change the rule.

Source inventories and hashes are retained in `provenance/recorded_run/preflight_input_inventory.csv` and `provenance/recorded_run/preflight_preflight.json`. These describe the inputs recorded for the experiment and do not authorize redistribution. The package includes the applicable source notices and documented modifications. Sharing these aggregates does not claim that the complete raw-product preparation pipeline has been reconstructed.

## Coastline handling

The author identifies GADM with Cartopy and a 5 km boundary buffer as the map source and method. The original recovered `coast` array had 14,301 longitude/latitude line segments. Option 2 removes that array from the distributed plotting NPZ and excludes the standalone Figure 1 PDF. Original copies are preserved outside the public payload; the manuscript's map remains unchanged.

[GADM's terms](https://gadm.org/license.html) permit academic article maps but generally require prior permission for data redistribution or commercial use. No GADM boundary coordinates are proposed for this public package. `analysis/reproduce_figures.py` skips Figure 1 without a user-supplied local coastline file and still regenerates the other main figures. Source attribution and the exact packaging changes are recorded in `../provenance/COASTLINE_SOURCE.md` and `../provenance/CURRENT_TRANSFORMATIONS.json`.

This coastline decision does not authenticate hotspot point binning, sensor continuity or filters. See `SOURCE_ATTRIBUTION.md` for the model-input sources and remaining qualifications. Software licensing remains separate from data rights.
