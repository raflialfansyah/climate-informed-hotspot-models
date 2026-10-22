# Reproducibility levels and boundaries

| Task | Required inputs | Status |
|---|---|---|
| Read all result tables | This folder | Available |
| Recalculate 105 x 15 main metrics | Packaged predictions and tables | Verified without fitting |
| Reconstruct 81 features under all four schedules | Included regional CSVs, full SST context and main environment | Verified against the original preflight; zero fitting or inference |
| Retrain the main, ablation and earlier-window scheme | Included processed inputs and main modeling dependencies | Input route provided; 371 production fits are not repeated for packaging |
| Regenerate non-map main figures and seven regional diagnostic panels | Packaged CSVs and coastline-free plotting NPZ | Available through `analysis/reproduce_figures.py` |
| Regenerate Figure 1 | Packaged count/grid inputs plus authorized local coastline NPZ | Coastline and standalone original map PDF excluded; no automatic download or substitution |
| Check individual-feature summaries | Included procedure exports | Available without fitted models |
| Repeat individual-feature perturbation inference | Original external fitted snapshots and trusted preflight | Not distributed; configure local authorized paths |
| Reconstruct every upstream gridded product from downloads | Complete producer versions, rules and source files | Not an established end-to-end pipeline |

The default notebook input route is processed CSV. The optional raw route retains the original source aggregation code. Both call the same feature, fitting, calibration, inversion and reporting functions. Input identities differ, so source changes require fresh caches and experiments. Exporting an aggregate preserves the recorded scientific input but does not verify its original source processing.

`requirements.txt` supports result checking and plotting. `requirements-main.txt` records direct local modeling dependencies, and `requirements-recorded-run.txt` records original training versions. They are not complete transitive locks. The original run used TensorFlow 2.21.0 with a GPU; local checks use TensorFlow 2.20.0 on CPU. Matching feature values does not promise bitwise-identical retraining on different devices or dependencies.

Author-supplied MATLAB scripts now document OISST v2.1, regions, arithmetic spatial means and historical anomaly construction; see `../provenance/oisst/README.md`. Their raw SST columns exactly match the included context. The 2000-file acquisition and MAT-to-CSV step are not shown, and original grids have not been reprocessed. The [hotspot MATLAB extraction script](../provenance/hotspot/README.md) also documents the record filters, spatial/day bins and zero fill, with no explicit deduplication or timezone conversion. Its grid matches the supplied MAT, but the original CSV was not reprocessed. Other qualifications remain for dry-spell stored-calendar correspondence, hotspot record metadata/sensor continuity and ERA5 evaporation timing. Source notices and data conditions are recorded in `SOURCE_ATTRIBUTION.md`. Processed input inclusion does not establish an untouched confirmatory test record or independently authenticate original download requests.

`COPY_MANIFEST.json` records the initial copies. `CURRENT_TRANSFORMATIONS.json` records the explicit GADM exclusions and lossless retained-array checks. `RELEASE_MANIFEST.json` inventories the current public candidate, excluding private paths, local geometry, new experiment outputs and generated artifacts. Historical feature-importance flags describe the original main experiment; the later completed diagnostic is documented separately.
