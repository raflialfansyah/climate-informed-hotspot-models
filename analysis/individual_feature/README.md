# Individual-feature diagnostics

Complete results are available under `../../results/individual_feature/`. They cover all evaluation dates, 10 repeats and four perturbation settings, superseding the earlier pilot.

`run.py` ports the original frozen-inference runner. Its protocol, perturbation maps, formulas and accelerators are retained; bundle discovery now uses local configuration instead of historical working paths. Inputs are trusted main S5 snapshots and the original preflight cache. All estimator fitting calls are prohibited. New outputs go to `generated/individual_feature/`.

```text
python analysis/individual_feature/run.py --check-inputs
python analysis/individual_feature/run.py
```

Full inference can take considerable time and is unnecessary for reading saved results. The runner neither overwrites manuscript exports nor automatically replaces their results. Historical production validation is retained in `provenance/feature_independent_validation.json`. Full inference after the port has not been repeated; see the release validation report. Use the recorded environment versions. Only load pickle artifacts from the trusted original experiment.
