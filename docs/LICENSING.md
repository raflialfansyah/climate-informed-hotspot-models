# License scope

The project owner selected the MIT License for the software on 21 October 2026. The full text is provided in `../LICENSE`, following the [Open Source Initiative's MIT text](https://opensource.org/license/mit).

## Software covered by MIT

The MIT License applies to the code in `Hotspot_SameDay_Main.ipynb`, `src/` and `analysis/`, together with notebook instructions, the repository README, software guides, dependency specifications and configuration examples. The copyright notice uses the collective description "Main same-day hotspot scheme contributors"; contributor attribution is recorded separately in `CITATION.cff`.

Retain the copyright and license notices when redistributing copies or substantial portions of the software. `CITATION.cff` provides academic citation information; MIT does not itself require citation of the associated paper.

The author-supplied hotspot extraction code in `provenance/hotspot/A1_Ekstraksi_Harian.m` is also covered by the project's MIT software license. Its referenced FIRMS records and optional coastline files retain their separate source conditions and are not included with the script.

## Materials outside the software license

The MIT software license does not grant new rights over datasets or data-derived exports in `data/` and `results/`, scientific reports in `reports/`, figure assets and coastline geometry in `figures/` or the plotting NPZ, or third-party source materials referenced by provenance records. The README files describing these folders are software guides and are covered by MIT; the underlying data and scientific assets are not thereby relicensed.

These materials retain applicable source rights and conditions. In particular, processed ERA5 fields retain the source CC BY 4.0 conditions and the attribution in `SOURCE_ATTRIBUTION.md`; NASA and NOAA material follows its applicable source policies. No blanket MIT or new data/content licence is applied to all scientific assets. Availability of a local file does not override third-party terms. Consult `DATA_AVAILABILITY.md` for source status and `PUBLICATION_CHECKLIST.md` for remaining release tasks.


## GADM boundary geometry

The author identifies GADM as the source for the coastline display, with Cartopy and a 5 km boundary-buffer method; see `../provenance/COASTLINE_SOURCE.md`. [GADM's terms](https://gadm.org/license.html), checked on 21 October 2026, permit academic/non-commercial use and article maps, while requiring prior permission for data redistribution or commercial use. The MIT software license does not override these conditions or establish permission to redistribute the recovered or buffered geometry. Option 2 excludes those coordinates and the standalone original map PDF from the public payload; any local reintroduction remains subject to the applicable terms. No separate license is granted here for figure or data assets.

Processed input CSVs are included as a local publication candidate with their source qualifications. They are not relicensed under MIT. Consult `SOURCE_ATTRIBUTION.md` for source notices and source attribution, modification notices and remaining historical metadata qualifications.
