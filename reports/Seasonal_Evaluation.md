# Rainfall-defined seasonal evaluation

E02, Reviewer 3 temporal coverage and seasonality. 11 October 2026.

**All 13 main models have now been evaluated separately in regional dry and wet rainfall states using an external rule. The labels are an adaptation to regional mean CMORPH rainfall, not independently observed official BMKG ZOM seasons.**

The primary definition was frozen before seasonal model scoring. It uses no hotspot counts, predictions, errors or rankings. The rain series is the same study input; an external rule does not make it an independent rainfall observation product. Results are conditional diagnostics of the existing all-year models, not dry-season-only training or a causal seasonal effect.

## Published basis and implemented adaptation

BMKG defines calendar dasarians as days 1-10, 11-20 and 21-month end, and uses a 50 mm threshold with persistence to identify dry/wet onset. Its seasonal information is defined for rainfall zones, which need not coincide with administrative areas. These facts support a rainfall-based stratification but do not make the seven study rectangles official seasonal zones. [BMKG glossary](https://bbmkg3.bmkg.go.id/daftar-istilah-musim), [BMKG 2024 explanation](https://www.bmkg.go.id/siaran-pers/hujan-di-musim-kemarau-bmkg-normal-terjadi-bukan-anomali-iklim).

The primary conservative rule requires three consecutive dasarians each below 50 mm for dry onset, or each at least 50 mm for wet onset. The label starts at the first confirming block and is carried until an opposite confirmed onset. Actual block totals are used even though the final calendar dasarian varies in length. State construction starts in 2001 and does not reset at January or the 2019 evaluation boundary. Before the first qualifying onset and in the final two source dasarians, labels are unclassified. The latter comprise 21 days in December 2025 for every domain.

A fixed sensitivity rule also permits mixed blocks when the first is below/at least 50 mm and the three-block sum is below/at least 150 mm. Opposite onsets are accepted only after three blocks from the prior accepted onset to prevent overlapping confirmation windows; that state-extension choice is an explicit project adaptation. The source discusses seasonal-period criteria on printed p.2 and onset/dasarian definitions on printed p.6. The rule and sensitivity are reported together, without choosing the one giving favorable model metrics. [BMKG PMH 2023/2024](https://stamet-kotim.bmkg.go.id/wp-content/uploads/2023/09/PMH-2023_2024-Kalteng.pdf).

Indonesia has distinct rainfall regimes, so no single May-September or DJF/JJA calendar is imposed on all regions. This is especially relevant to the national aggregate and broad Kalimantan/Sulawesi/Papua rectangles. The labels describe their aggregated rainfall, not simultaneous dry conditions at every cell or the fraction of land in a dry season. The inherited support and missing authenticated land mask/source-retrieval records remain qualifications. [Aldrian and Susanto, 2003](https://www2.atmos.umd.edu/~dwi/papers/aldrian_susanto_ijc.pdf).

The forward confirmation uses later rainfall and is retrospective. No label was added as a predictor or used to fit, calibrate or choose a model. It supplies no operational onset forecast. A wet day can occur within a carried dry state; the method labels persistent periods rather than thresholding individual days.

## Evaluation and uncertainty

Scope: all 13 fitted main S5 models in seven domains on 2019-2025, plus saved persistence and training-only monthly climatology references. Seeds and chosen inversions remain unchanged. Every model sees the same season dates within a domain. The main count threshold is retained from the raw through-2014 training 90th percentile and is not re-estimated on dry or wet observations. MAE90/RMSE90 therefore retain their original meaning. All 15 metrics are reported, including event rates/counts and zero-day false detections.

The all-year metrics were independently recomputed and match all 91 main results. Dry, wet and unclassified strata partition the 2,557 dates exactly; their sample counts, observed totals, event counts and absolute/squared error sums reconstruct all-year results. Unclassified observations remain in all-year evaluation and have separate exported diagnostics. Scores for no high days or zero-denominator rates remain NA.

Primary-rule absolute and paired-reference intervals use 500 whole-year draws with seed 42 and unadjusted 95% percentile limits, conditional on fitted predictions and this season rule. All seven calendar years are sampled, including years containing zero days of a particular state; finite-resample counts and actual years with season/high-day support are exported. Few dry-support years, overlapping domains and multiple comparisons limit inference. These are not daily prediction intervals and do not include rainfall-product or season-definition uncertainty. Reference differences match dates within the same state. Dry-minus-wet differences concern different observed populations and are descriptive, not matched causal effects.

## Coverage under the primary rule

| Domain | Dry days | Wet days | Unclassified days | Dry share % | High days dry | High days wet | Dry hotspot-total share % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| National | 430 | 2106 | 21 | 16.8 | 75 | 2 | 79.3 |
| North Sumatra | 239 | 2297 | 21 | 9.3 | 14 | 31 | 29.2 |
| South Sumatra | 296 | 2240 | 21 | 11.6 | 99 | 13 | 87.1 |
| Kalimantan | 123 | 2413 | 21 | 4.8 | 41 | 52 | 48.0 |
| Sulawesi | 671 | 1865 | 21 | 26.2 | 128 | 21 | 85.5 |
| Nusa Tenggara | 1963 | 573 | 21 | 76.8 | 204 | 0 | 99.6 |
| Papua | 234 | 2302 | 21 | 9.2 | 100 | 85 | 59.7 |

Dry-day and hotspot shares refer to the full 2019-2025 record, including unclassified days in the denominator. A high-hotspot day may occur in a region-mean wet state. Regional mean rainfall cannot identify every local dry pocket or fire mechanism.

## Definition sensitivity

| Domain | Changed labels / 2557 | Primary dry days | Mixed-rule dry days | Primary MLP dry RMSE | Mixed-rule MLP dry RMSE |
| --- | --- | --- | --- | --- | --- |
| National | 182 | 430 | 446 | 111.026 | 106.680 |
| North Sumatra | 263 | 239 | 398 | 14.951 | 9.525 |
| South Sumatra | 174 | 296 | 410 | 74.939 | 63.742 |
| Kalimantan | 31 | 123 | 154 | 83.805 | 75.091 |
| Sulawesi | 263 | 671 | 690 | 4.383 | 4.322 |
| Nusa Tenggara | 320 | 1963 | 1809 | 4.159 | 4.333 |
| Papua | 163 | 234 | 337 | 14.312 | 10.625 |

Changing a label changes the scored observation population. This table is a definition sensitivity, not a matched model improvement. Complete sensitivity metrics for every model are exported; official ZOM validation remains unperformed.

## What the seasonal results show

All 91 model-domain comparisons have larger raw count RMSE in the dry state than in the wet state. Ratios range from 2.08 to 28.28. This reflects evaluation on different activity distributions and is not evidence that a season label causes model deterioration. The all-year results and chosen inversions are unchanged.

Nationally, 430 dry-state days (16.8% of the evaluation record) contain 79.3% of observed hotspots and 75 of 77 high-hotspot days. This supports reporting dry-state diagnostics alongside all-year results, rather than relying on all-year errors alone. It does not imply that all regional high-hotspot days occur in dry states: North Sumatra has 31 high days in wet states versus 14 in dry states, and Kalimantan has 52 versus 41.

The dry state has observations in only two evaluation years in South Sumatra, Kalimantan and Papua. Year-block intervals for these subsets have limited effective support. Nusa Tenggara's wet state contains 573 days but only 13 hotspots in total and no high days. Its wet-state MAE90, RMSE90 and POD are unavailable; FAR and CSI additionally depend on whether a model predicts any high events. Low wet-state errors there offer limited evidence about performance during fire activity.

Against persistence, 89 of 91 dry-state model-domain comparisons have lower point RMSE, with 74 conditional paired intervals entirely below zero. Against monthly climatology, the corresponding counts are 89 and 80. These are descriptive counts across overlapping regions/models, without multiplicity correction. In Nusa Tenggara's sparse wet state, none of the 13 models has lower RMSE than persistence. Favorable dry-state reference comparisons do not establish uniformly superior event detection or temporal robustness.

The sensitivity rule changes 31 to 320 date labels per domain. Every sensitivity value is reported without replacing the primary rule. Because this changes the scored population, lower sensitivity RMSE is not an improved model result. Region-mean labels are especially sensitive to spatial averaging; the dry-state percentages should not be interpreted as official seasonal-zone coverage.

| Domain | Dry-support years / 7 | High-day dry-support years / 7 | Minimum dry/wet RMSE ratio | Maximum dry/wet RMSE ratio |
| --- | --- | --- | --- | --- |
| National | 4 | 3 | 5.81 | 11.21 |
| North Sumatra | 4 | 3 | 2.08 | 2.83 |
| South Sumatra | 2 | 2 | 15.39 | 28.28 |
| Kalimantan | 2 | 2 | 3.69 | 7.71 |
| Sulawesi | 5 | 5 | 7.55 | 8.87 |
| Nusa Tenggara | 7 | 7 | 12.11 | 19.22 |
| Papua | 2 | 2 | 3.90 | 5.04 |

![Year-specific rainfall-defined dry-state coverage](D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/dry_state_coverage.png)

Each cell is dry-state days divided by calendar days in that year. A displayed zero means no qualifying region-mean dry state under this rule, not proof that every local area remained wet. Integer percentages are rounded.

![Dry/wet RMSE ratios for all 13 models](D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/dry_wet_rmse_ratio.png)

Cell labels are ratios; colors show their base-10 logarithms. Values above one indicate larger errors on the dry-state population. Populations differ, so these are descriptive ratios. The figures are available as vector PDFs for manuscript integration.

## Complete primary-rule model metrics

Within each region, Dry and Wet entries refer to its rainfall-defined states. Count errors and bias are hotspot counts, SMAPE is percent and POD/FAR/CSI range 0-1. Full-precision values, annual strata and unclassified diagnostics are in the CSVs. No winner is chosen from these retrospective tables.

### National

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 109.672 | 48.263 | 0.558 | 172.566 | 251.078 |
| RandomForest | Wet | 10.027 | 3.868 | 0.304 | 173.226 | 181.619 |
| ExtraTrees | Dry | 112.258 | 48.494 | 0.537 | 175.100 | 257.749 |
| ExtraTrees | Wet | 10.015 | 3.837 | 0.306 | 172.243 | 181.388 |
| XGBoost | Dry | 107.781 | 49.573 | 0.573 | 163.317 | 242.161 |
| XGBoost | Wet | 10.298 | 3.899 | 0.266 | 162.933 | 175.297 |
| LightGBM | Dry | 110.509 | 50.384 | 0.551 | 168.650 | 249.533 |
| LightGBM | Wet | 10.348 | 3.962 | 0.259 | 165.255 | 176.434 |
| SVM_RBF | Dry | 139.535 | 65.415 | 0.284 | 235.464 | 319.255 |
| SVM_RBF | Wet | 14.404 | 5.331 | -0.436 | 182.311 | 188.567 |
| KNN | Dry | 129.715 | 58.488 | 0.381 | 199.112 | 295.163 |
| KNN | Wet | 11.856 | 4.440 | 0.027 | 187.075 | 191.175 |
| BayesianRidge | Dry | 82.665 | 40.212 | 0.749 | 135.222 | 184.176 |
| BayesianRidge | Wet | 9.862 | 3.643 | 0.327 | 171.691 | 181.348 |
| MLP_Model_1 | Dry | 103.867 | 58.327 | 0.603 | 141.791 | 209.275 |
| MLP_Model_1 | Wet | 17.880 | 6.634 | -1.212 | 164.941 | 177.791 |
| MLP_Model_2 | Dry | 111.026 | 55.592 | 0.547 | 158.887 | 243.687 |
| MLP_Model_2 | Wet | 12.948 | 6.434 | -0.160 | 174.218 | 182.100 |
| MLP_Model_3 | Dry | 100.573 | 60.284 | 0.628 | 138.275 | 189.224 |
| MLP_Model_3 | Wet | 12.356 | 6.059 | -0.056 | 175.732 | 182.559 |
| MLP_Model_4 | Dry | 109.766 | 52.201 | 0.557 | 173.283 | 248.303 |
| MLP_Model_4 | Wet | 11.133 | 5.780 | 0.142 | 168.646 | 178.672 |
| Poisson | Dry | 83.019 | 44.831 | 0.747 | 126.449 | 173.412 |
| Poisson | Wet | 10.620 | 5.059 | 0.220 | 148.970 | 169.139 |
| Tweedie | Dry | 85.935 | 44.724 | 0.728 | 133.025 | 185.923 |
| Tweedie | Wet | 10.434 | 4.741 | 0.247 | 161.717 | 173.999 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -21.677 | 60.008 | 0.547 | 0.226 | 0.471 |
| RandomForest | Wet | -0.563 | 112.460 | 0.000 | NA | 0.000 |
| ExtraTrees | Dry | -21.844 | 59.319 | 0.547 | 0.212 | 0.477 |
| ExtraTrees | Wet | -0.664 | 112.641 | 0.000 | NA | 0.000 |
| XGBoost | Dry | -13.522 | 60.912 | 0.560 | 0.300 | 0.452 |
| XGBoost | Wet | -0.269 | 113.594 | 0.000 | NA | 0.000 |
| LightGBM | Dry | -14.256 | 60.741 | 0.587 | 0.323 | 0.458 |
| LightGBM | Wet | -0.166 | 113.639 | 0.000 | NA | 0.000 |
| SVM_RBF | Dry | -33.228 | 81.294 | 0.387 | 0.275 | 0.337 |
| SVM_RBF | Wet | 1.180 | 116.255 | 0.000 | 1.000 | 0.000 |
| KNN | Dry | -20.077 | 69.758 | 0.467 | 0.314 | 0.385 |
| KNN | Wet | -0.097 | 117.269 | 0.000 | 1.000 | 0.000 |
| BayesianRidge | Dry | -8.331 | 56.511 | 0.560 | 0.208 | 0.488 |
| BayesianRidge | Wet | -0.786 | 110.401 | 0.000 | NA | 0.000 |
| MLP_Model_1 | Dry | 15.587 | 71.521 | 0.707 | 0.470 | 0.434 |
| MLP_Model_1 | Wet | 3.665 | 120.676 | 0.000 | 1.000 | 0.000 |
| MLP_Model_2 | Dry | -2.676 | 70.305 | 0.587 | 0.450 | 0.396 |
| MLP_Model_2 | Wet | 3.339 | 123.512 | 0.000 | 1.000 | 0.000 |
| MLP_Model_3 | Dry | 22.541 | 73.875 | 0.787 | 0.482 | 0.454 |
| MLP_Model_3 | Wet | 3.114 | 121.975 | 0.000 | 1.000 | 0.000 |
| MLP_Model_4 | Dry | -14.368 | 67.701 | 0.533 | 0.310 | 0.430 |
| MLP_Model_4 | Wet | 2.541 | 121.779 | 0.000 | NA | 0.000 |
| Poisson | Dry | 5.571 | 62.629 | 0.613 | 0.370 | 0.451 |
| Poisson | Wet | 2.400 | 116.478 | 0.000 | NA | 0.000 |
| Tweedie | Dry | 3.158 | 62.784 | 0.547 | 0.317 | 0.436 |
| Tweedie | Wet | 1.820 | 114.793 | 0.000 | NA | 0.000 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 41 | 34 | 12 | 343 | 0 |
| RandomForest | Wet | 0 | 2 | 0 | 2104 | 0 |
| ExtraTrees | Dry | 41 | 34 | 11 | 344 | 0 |
| ExtraTrees | Wet | 0 | 2 | 0 | 2104 | 0 |
| XGBoost | Dry | 42 | 33 | 18 | 337 | 0 |
| XGBoost | Wet | 0 | 2 | 0 | 2104 | 0 |
| LightGBM | Dry | 44 | 31 | 21 | 334 | 0 |
| LightGBM | Wet | 0 | 2 | 0 | 2104 | 0 |
| SVM_RBF | Dry | 29 | 46 | 11 | 344 | 0 |
| SVM_RBF | Wet | 0 | 2 | 5 | 2099 | 0 |
| KNN | Dry | 35 | 40 | 16 | 339 | 0 |
| KNN | Wet | 0 | 2 | 1 | 2103 | 0 |
| BayesianRidge | Dry | 42 | 33 | 11 | 344 | 0 |
| BayesianRidge | Wet | 0 | 2 | 0 | 2104 | 0 |
| MLP_Model_1 | Dry | 53 | 22 | 47 | 308 | 0 |
| MLP_Model_1 | Wet | 0 | 2 | 5 | 2099 | 0 |
| MLP_Model_2 | Dry | 44 | 31 | 36 | 319 | 0 |
| MLP_Model_2 | Wet | 0 | 2 | 4 | 2100 | 0 |
| MLP_Model_3 | Dry | 59 | 16 | 55 | 300 | 0 |
| MLP_Model_3 | Wet | 0 | 2 | 3 | 2101 | 0 |
| MLP_Model_4 | Dry | 40 | 35 | 18 | 337 | 0 |
| MLP_Model_4 | Wet | 0 | 2 | 0 | 2104 | 0 |
| Poisson | Dry | 46 | 29 | 27 | 328 | 0 |
| Poisson | Wet | 0 | 2 | 0 | 2104 | 0 |
| Tweedie | Dry | 41 | 34 | 19 | 336 | 0 |
| Tweedie | Wet | 0 | 2 | 0 | 2104 | 0 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 12 | 9 |
| Dry | MonthlyClimatology | 13 | 13 |
| Wet | Persistence | 11 | 8 |
| Wet | MonthlyClimatology | 13 | 13 |

### North Sumatra

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 13.571 | 6.712 | 0.376 | 34.441 | 41.554 |
| RandomForest | Wet | 6.153 | 2.295 | 0.498 | 32.292 | 39.457 |
| ExtraTrees | Dry | 13.287 | 6.480 | 0.402 | 35.670 | 43.146 |
| ExtraTrees | Wet | 6.225 | 2.219 | 0.486 | 32.693 | 40.473 |
| XGBoost | Dry | 13.524 | 5.746 | 0.381 | 35.305 | 44.055 |
| XGBoost | Wet | 6.274 | 1.720 | 0.478 | 29.688 | 37.361 |
| LightGBM | Dry | 13.060 | 5.607 | 0.422 | 35.150 | 43.638 |
| LightGBM | Wet | 6.167 | 1.712 | 0.496 | 30.810 | 38.898 |
| SVM_RBF | Dry | 21.049 | 9.234 | -0.501 | 42.029 | 51.483 |
| SVM_RBF | Wet | 7.434 | 2.080 | 0.267 | 46.499 | 56.120 |
| KNN | Dry | 16.091 | 7.771 | 0.123 | 35.378 | 45.566 |
| KNN | Wet | 7.614 | 2.737 | 0.231 | 41.448 | 52.044 |
| BayesianRidge | Dry | 12.119 | 5.416 | 0.503 | 35.451 | 43.812 |
| BayesianRidge | Wet | 5.828 | 1.996 | 0.550 | 32.297 | 39.876 |
| MLP_Model_1 | Dry | 16.157 | 8.133 | 0.116 | 34.322 | 41.757 |
| MLP_Model_1 | Wet | 7.328 | 2.530 | 0.288 | 35.785 | 45.346 |
| MLP_Model_2 | Dry | 14.951 | 6.832 | 0.243 | 35.585 | 44.310 |
| MLP_Model_2 | Wet | 6.610 | 1.974 | 0.420 | 39.749 | 47.874 |
| MLP_Model_3 | Dry | 15.527 | 7.336 | 0.183 | 37.282 | 46.033 |
| MLP_Model_3 | Wet | 6.971 | 2.395 | 0.355 | 41.363 | 50.118 |
| MLP_Model_4 | Dry | 15.076 | 6.980 | 0.230 | 40.492 | 47.837 |
| MLP_Model_4 | Wet | 6.718 | 2.043 | 0.401 | 36.256 | 44.095 |
| Poisson | Dry | 13.873 | 7.161 | 0.348 | 34.984 | 42.689 |
| Poisson | Wet | 6.435 | 2.537 | 0.451 | 25.056 | 31.737 |
| Tweedie | Dry | 13.377 | 6.372 | 0.394 | 36.729 | 43.636 |
| Tweedie | Wet | 6.196 | 2.322 | 0.491 | 28.096 | 35.954 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 1.535 | 123.511 | 0.429 | 0.647 | 0.240 |
| RandomForest | Wet | 0.871 | 166.037 | 0.548 | 0.414 | 0.395 |
| ExtraTrees | Dry | 1.036 | 123.016 | 0.357 | 0.667 | 0.208 |
| ExtraTrees | Wet | 0.786 | 165.998 | 0.484 | 0.483 | 0.333 |
| XGBoost | Dry | 0.337 | 120.299 | 0.357 | 0.667 | 0.208 |
| XGBoost | Wet | 0.172 | 159.637 | 0.581 | 0.438 | 0.400 |
| LightGBM | Dry | 0.161 | 120.478 | 0.357 | 0.643 | 0.217 |
| LightGBM | Wet | 0.121 | 163.659 | 0.548 | 0.452 | 0.378 |
| SVM_RBF | Dry | 2.306 | 130.656 | 0.214 | 0.864 | 0.091 |
| SVM_RBF | Wet | -0.080 | 140.684 | 0.194 | 0.625 | 0.146 |
| KNN | Dry | 2.192 | 128.569 | 0.500 | 0.682 | 0.241 |
| KNN | Wet | 1.008 | 167.217 | 0.387 | 0.684 | 0.211 |
| BayesianRidge | Dry | 0.019 | 118.306 | 0.357 | 0.286 | 0.312 |
| BayesianRidge | Wet | 0.510 | 152.412 | 0.548 | 0.433 | 0.386 |
| MLP_Model_1 | Dry | 3.914 | 130.426 | 0.643 | 0.654 | 0.290 |
| MLP_Model_1 | Wet | 0.993 | 168.847 | 0.419 | 0.519 | 0.289 |
| MLP_Model_2 | Dry | 0.944 | 131.369 | 0.357 | 0.667 | 0.208 |
| MLP_Model_2 | Wet | 0.026 | 174.686 | 0.387 | 0.520 | 0.273 |
| MLP_Model_3 | Dry | 2.313 | 127.035 | 0.357 | 0.706 | 0.192 |
| MLP_Model_3 | Wet | 0.656 | 169.352 | 0.290 | 0.526 | 0.220 |
| MLP_Model_4 | Dry | 0.622 | 133.146 | 0.429 | 0.571 | 0.273 |
| MLP_Model_4 | Wet | 0.291 | 174.739 | 0.484 | 0.516 | 0.319 |
| Poisson | Dry | 2.859 | 126.819 | 0.571 | 0.600 | 0.308 |
| Poisson | Wet | 1.521 | 167.694 | 0.742 | 0.465 | 0.451 |
| Tweedie | Dry | 1.376 | 122.866 | 0.429 | 0.500 | 0.300 |
| Tweedie | Wet | 1.076 | 167.342 | 0.613 | 0.513 | 0.373 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 6 | 8 | 11 | 214 | 0 |
| RandomForest | Wet | 17 | 14 | 12 | 2254 | 0 |
| ExtraTrees | Dry | 5 | 9 | 10 | 215 | 0 |
| ExtraTrees | Wet | 15 | 16 | 14 | 2252 | 0 |
| XGBoost | Dry | 5 | 9 | 10 | 215 | 0 |
| XGBoost | Wet | 18 | 13 | 14 | 2252 | 0 |
| LightGBM | Dry | 5 | 9 | 9 | 216 | 0 |
| LightGBM | Wet | 17 | 14 | 14 | 2252 | 0 |
| SVM_RBF | Dry | 3 | 11 | 19 | 206 | 1 |
| SVM_RBF | Wet | 6 | 25 | 10 | 2256 | 0 |
| KNN | Dry | 7 | 7 | 15 | 210 | 1 |
| KNN | Wet | 12 | 19 | 26 | 2240 | 1 |
| BayesianRidge | Dry | 5 | 9 | 2 | 223 | 0 |
| BayesianRidge | Wet | 17 | 14 | 13 | 2253 | 0 |
| MLP_Model_1 | Dry | 9 | 5 | 17 | 208 | 0 |
| MLP_Model_1 | Wet | 13 | 18 | 14 | 2252 | 1 |
| MLP_Model_2 | Dry | 5 | 9 | 10 | 215 | 1 |
| MLP_Model_2 | Wet | 12 | 19 | 13 | 2253 | 0 |
| MLP_Model_3 | Dry | 5 | 9 | 12 | 213 | 0 |
| MLP_Model_3 | Wet | 9 | 22 | 10 | 2256 | 0 |
| MLP_Model_4 | Dry | 6 | 8 | 8 | 217 | 0 |
| MLP_Model_4 | Wet | 15 | 16 | 16 | 2250 | 0 |
| Poisson | Dry | 8 | 6 | 12 | 213 | 0 |
| Poisson | Wet | 23 | 8 | 20 | 2246 | 1 |
| Tweedie | Dry | 6 | 8 | 6 | 219 | 0 |
| Tweedie | Wet | 19 | 12 | 20 | 2246 | 0 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 12 | 0 |
| Dry | MonthlyClimatology | 13 | 12 |
| Wet | Persistence | 13 | 6 |
| Wet | MonthlyClimatology | 13 | 13 |

### South Sumatra

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 63.481 | 25.189 | 0.290 | 64.615 | 108.872 |
| RandomForest | Wet | 2.508 | 0.809 | 0.260 | 23.042 | 24.991 |
| ExtraTrees | Dry | 63.108 | 25.362 | 0.299 | 63.562 | 107.966 |
| ExtraTrees | Wet | 2.532 | 0.812 | 0.246 | 23.193 | 25.186 |
| XGBoost | Dry | 62.463 | 25.047 | 0.313 | 62.847 | 106.895 |
| XGBoost | Wet | 2.528 | 0.828 | 0.248 | 19.238 | 22.211 |
| LightGBM | Dry | 62.468 | 25.170 | 0.313 | 63.163 | 106.828 |
| LightGBM | Wet | 2.534 | 0.824 | 0.245 | 19.441 | 22.157 |
| SVM_RBF | Dry | 69.701 | 27.189 | 0.144 | 70.480 | 119.809 |
| SVM_RBF | Wet | 3.188 | 0.987 | -0.196 | 21.669 | 23.948 |
| KNN | Dry | 65.616 | 27.195 | 0.242 | 67.601 | 112.375 |
| KNN | Wet | 2.714 | 0.865 | 0.133 | 26.064 | 27.434 |
| BayesianRidge | Dry | 54.181 | 23.310 | 0.483 | 56.261 | 91.516 |
| BayesianRidge | Wet | 2.588 | 0.841 | 0.212 | 24.511 | 26.152 |
| MLP_Model_1 | Dry | 59.152 | 26.546 | 0.384 | 59.180 | 97.996 |
| MLP_Model_1 | Wet | 3.012 | 0.899 | -0.067 | 20.751 | 22.649 |
| MLP_Model_2 | Dry | 74.939 | 28.400 | 0.011 | 77.142 | 129.333 |
| MLP_Model_2 | Wet | 2.650 | 0.742 | 0.174 | 24.393 | 26.183 |
| MLP_Model_3 | Dry | 59.745 | 26.770 | 0.371 | 63.251 | 100.977 |
| MLP_Model_3 | Wet | 3.883 | 1.089 | -0.773 | 20.907 | 22.531 |
| MLP_Model_4 | Dry | 61.292 | 26.499 | 0.338 | 60.438 | 102.082 |
| MLP_Model_4 | Wet | 3.249 | 0.993 | -0.242 | 21.120 | 23.438 |
| Poisson | Dry | 57.230 | 25.152 | 0.423 | 56.485 | 95.032 |
| Poisson | Wet | 2.978 | 1.421 | -0.043 | 20.018 | 22.728 |
| Tweedie | Dry | 57.934 | 24.740 | 0.409 | 57.901 | 97.539 |
| Tweedie | Wet | 2.697 | 1.139 | 0.144 | 21.431 | 23.949 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -17.352 | 103.606 | 0.616 | 0.228 | 0.521 |
| RandomForest | Wet | -0.118 | 182.877 | 0.000 | NA | 0.000 |
| ExtraTrees | Dry | -16.033 | 103.486 | 0.697 | 0.242 | 0.570 |
| ExtraTrees | Wet | -0.108 | 183.086 | 0.000 | NA | 0.000 |
| XGBoost | Dry | -15.766 | 102.939 | 0.657 | 0.235 | 0.546 |
| XGBoost | Wet | 0.013 | 168.328 | 0.308 | 0.333 | 0.267 |
| LightGBM | Dry | -15.441 | 104.220 | 0.677 | 0.272 | 0.540 |
| LightGBM | Wet | 0.003 | 169.622 | 0.154 | 0.667 | 0.118 |
| SVM_RBF | Dry | -21.927 | 111.376 | 0.434 | 0.232 | 0.384 |
| SVM_RBF | Wet | 0.130 | 132.397 | 0.154 | 0.846 | 0.083 |
| KNN | Dry | -17.988 | 115.382 | 0.566 | 0.325 | 0.444 |
| KNN | Wet | -0.148 | 155.557 | 0.000 | 1.000 | 0.000 |
| BayesianRidge | Dry | -8.312 | 99.909 | 0.778 | 0.252 | 0.616 |
| BayesianRidge | Wet | -0.041 | 133.606 | 0.000 | NA | 0.000 |
| MLP_Model_1 | Dry | -5.867 | 112.362 | 0.798 | 0.319 | 0.581 |
| MLP_Model_1 | Wet | 0.031 | 185.982 | 0.231 | 0.769 | 0.130 |
| MLP_Model_2 | Dry | -25.086 | 114.803 | 0.414 | 0.163 | 0.383 |
| MLP_Model_2 | Wet | -0.310 | 190.473 | 0.000 | NA | 0.000 |
| MLP_Model_3 | Dry | -6.605 | 108.275 | 0.828 | 0.287 | 0.621 |
| MLP_Model_3 | Wet | 0.293 | 184.144 | 0.154 | 0.905 | 0.062 |
| MLP_Model_4 | Dry | -5.988 | 107.859 | 0.818 | 0.314 | 0.596 |
| MLP_Model_4 | Wet | 0.138 | 186.142 | 0.231 | 0.769 | 0.130 |
| Poisson | Dry | -4.855 | 100.813 | 0.828 | 0.317 | 0.599 |
| Poisson | Wet | 0.833 | 176.441 | 0.231 | 0.750 | 0.136 |
| Tweedie | Dry | -9.105 | 101.696 | 0.788 | 0.310 | 0.582 |
| Tweedie | Wet | 0.434 | 177.733 | 0.077 | 0.750 | 0.062 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 61 | 38 | 18 | 179 | 0 |
| RandomForest | Wet | 0 | 13 | 0 | 2227 | 0 |
| ExtraTrees | Dry | 69 | 30 | 22 | 175 | 0 |
| ExtraTrees | Wet | 0 | 13 | 0 | 2227 | 0 |
| XGBoost | Dry | 65 | 34 | 20 | 177 | 0 |
| XGBoost | Wet | 4 | 9 | 2 | 2225 | 0 |
| LightGBM | Dry | 67 | 32 | 25 | 172 | 0 |
| LightGBM | Wet | 2 | 11 | 4 | 2223 | 0 |
| SVM_RBF | Dry | 43 | 56 | 13 | 184 | 0 |
| SVM_RBF | Wet | 2 | 11 | 11 | 2216 | 1 |
| KNN | Dry | 56 | 43 | 27 | 170 | 2 |
| KNN | Wet | 0 | 13 | 1 | 2226 | 0 |
| BayesianRidge | Dry | 77 | 22 | 26 | 171 | 0 |
| BayesianRidge | Wet | 0 | 13 | 0 | 2227 | 0 |
| MLP_Model_1 | Dry | 79 | 20 | 37 | 160 | 1 |
| MLP_Model_1 | Wet | 3 | 10 | 10 | 2217 | 2 |
| MLP_Model_2 | Dry | 41 | 58 | 8 | 189 | 0 |
| MLP_Model_2 | Wet | 0 | 13 | 0 | 2227 | 0 |
| MLP_Model_3 | Dry | 82 | 17 | 33 | 164 | 1 |
| MLP_Model_3 | Wet | 2 | 11 | 19 | 2208 | 3 |
| MLP_Model_4 | Dry | 81 | 18 | 37 | 160 | 1 |
| MLP_Model_4 | Wet | 3 | 10 | 10 | 2217 | 1 |
| Poisson | Dry | 82 | 17 | 38 | 159 | 0 |
| Poisson | Wet | 3 | 10 | 9 | 2218 | 0 |
| Tweedie | Dry | 78 | 21 | 35 | 162 | 0 |
| Tweedie | Wet | 1 | 12 | 3 | 2224 | 0 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 13 | 13 |
| Dry | MonthlyClimatology | 12 | 12 |
| Wet | Persistence | 13 | 12 |
| Wet | MonthlyClimatology | 13 | 13 |

### Kalimantan

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 105.487 | 50.624 | 0.643 | 117.742 | 176.908 |
| RandomForest | Wet | 17.640 | 4.489 | 0.564 | 77.606 | 106.922 |
| ExtraTrees | Dry | 112.515 | 53.147 | 0.594 | 126.597 | 190.110 |
| ExtraTrees | Wet | 17.714 | 4.419 | 0.560 | 78.362 | 108.920 |
| XGBoost | Dry | 123.215 | 54.734 | 0.513 | 136.057 | 209.443 |
| XGBoost | Wet | 18.955 | 4.116 | 0.496 | 79.555 | 114.623 |
| LightGBM | Dry | 130.389 | 56.848 | 0.454 | 141.995 | 221.635 |
| LightGBM | Wet | 17.926 | 4.012 | 0.549 | 76.645 | 107.270 |
| SVM_RBF | Dry | 181.846 | 85.065 | -0.062 | 208.853 | 306.012 |
| SVM_RBF | Wet | 23.594 | 4.679 | 0.219 | 102.282 | 153.172 |
| KNN | Dry | 135.775 | 66.417 | 0.408 | 146.845 | 228.515 |
| KNN | Wet | 21.335 | 5.231 | 0.362 | 83.392 | 131.773 |
| BayesianRidge | Dry | 136.649 | 59.636 | 0.401 | 152.304 | 234.068 |
| BayesianRidge | Wet | 27.104 | 4.624 | -0.030 | 99.291 | 178.687 |
| MLP_Model_1 | Dry | 109.569 | 53.611 | 0.615 | 126.799 | 184.727 |
| MLP_Model_1 | Wet | 20.260 | 5.363 | 0.424 | 90.431 | 125.026 |
| MLP_Model_2 | Dry | 83.805 | 49.367 | 0.775 | 100.514 | 132.627 |
| MLP_Model_2 | Wet | 22.479 | 5.464 | 0.291 | 91.612 | 118.611 |
| MLP_Model_3 | Dry | 132.711 | 57.712 | 0.435 | 146.095 | 227.644 |
| MLP_Model_3 | Wet | 18.342 | 4.716 | 0.528 | 86.209 | 117.746 |
| MLP_Model_4 | Dry | 110.707 | 61.608 | 0.607 | 133.920 | 180.586 |
| MLP_Model_4 | Wet | 28.895 | 5.925 | -0.171 | 121.227 | 180.224 |
| Poisson | Dry | 81.065 | 43.806 | 0.789 | 91.777 | 129.448 |
| Poisson | Wet | 21.961 | 5.390 | 0.324 | 87.411 | 130.825 |
| Tweedie | Dry | 101.014 | 50.061 | 0.672 | 115.324 | 169.366 |
| Tweedie | Wet | 23.203 | 4.785 | 0.245 | 92.669 | 148.291 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -21.402 | 88.346 | 0.878 | 0.217 | 0.706 |
| RandomForest | Wet | 0.024 | 156.068 | 0.538 | 0.364 | 0.412 |
| ExtraTrees | Dry | -24.890 | 88.653 | 0.878 | 0.250 | 0.679 |
| ExtraTrees | Wet | -0.051 | 156.426 | 0.538 | 0.391 | 0.400 |
| XGBoost | Dry | -30.435 | 88.653 | 0.829 | 0.190 | 0.694 |
| XGBoost | Wet | -1.069 | 155.786 | 0.462 | 0.400 | 0.353 |
| LightGBM | Dry | -32.910 | 89.363 | 0.854 | 0.186 | 0.714 |
| LightGBM | Wet | -1.113 | 156.504 | 0.462 | 0.385 | 0.358 |
| SVM_RBF | Dry | -38.622 | 106.728 | 0.537 | 0.371 | 0.407 |
| SVM_RBF | Wet | -1.561 | 137.974 | 0.327 | 0.433 | 0.262 |
| KNN | Dry | -22.319 | 99.155 | 0.927 | 0.406 | 0.567 |
| KNN | Wet | 0.469 | 157.364 | 0.596 | 0.415 | 0.419 |
| BayesianRidge | Dry | 19.008 | 86.274 | 0.878 | 0.143 | 0.766 |
| BayesianRidge | Wet | -0.105 | 142.211 | 0.462 | 0.294 | 0.387 |
| MLP_Model_1 | Dry | -18.941 | 91.919 | 0.927 | 0.240 | 0.717 |
| MLP_Model_1 | Wet | 1.541 | 157.952 | 0.558 | 0.431 | 0.392 |
| MLP_Model_2 | Dry | 5.395 | 95.600 | 0.927 | 0.309 | 0.655 |
| MLP_Model_2 | Wet | 1.694 | 161.004 | 0.538 | 0.451 | 0.373 |
| MLP_Model_3 | Dry | -39.140 | 91.125 | 0.902 | 0.178 | 0.755 |
| MLP_Model_3 | Wet | -0.508 | 156.207 | 0.385 | 0.310 | 0.328 |
| MLP_Model_4 | Dry | 22.308 | 97.725 | 0.951 | 0.328 | 0.650 |
| MLP_Model_4 | Wet | 1.840 | 160.586 | 0.500 | 0.435 | 0.361 |
| Poisson | Dry | 9.242 | 86.185 | 0.976 | 0.259 | 0.727 |
| Poisson | Wet | 1.547 | 157.385 | 0.538 | 0.451 | 0.373 |
| Tweedie | Dry | 18.120 | 85.721 | 0.927 | 0.283 | 0.679 |
| Tweedie | Wet | 0.509 | 157.506 | 0.519 | 0.400 | 0.386 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 36 | 5 | 10 | 72 | 0 |
| RandomForest | Wet | 28 | 24 | 16 | 2345 | 1 |
| ExtraTrees | Dry | 36 | 5 | 12 | 70 | 0 |
| ExtraTrees | Wet | 28 | 24 | 18 | 2343 | 1 |
| XGBoost | Dry | 34 | 7 | 8 | 74 | 0 |
| XGBoost | Wet | 24 | 28 | 16 | 2345 | 1 |
| LightGBM | Dry | 35 | 6 | 8 | 74 | 0 |
| LightGBM | Wet | 24 | 28 | 15 | 2346 | 1 |
| SVM_RBF | Dry | 22 | 19 | 13 | 69 | 1 |
| SVM_RBF | Wet | 17 | 35 | 13 | 2348 | 1 |
| KNN | Dry | 38 | 3 | 26 | 56 | 2 |
| KNN | Wet | 31 | 21 | 22 | 2339 | 0 |
| BayesianRidge | Dry | 36 | 5 | 6 | 76 | 0 |
| BayesianRidge | Wet | 24 | 28 | 10 | 2351 | 0 |
| MLP_Model_1 | Dry | 38 | 3 | 12 | 70 | 0 |
| MLP_Model_1 | Wet | 29 | 23 | 22 | 2339 | 1 |
| MLP_Model_2 | Dry | 38 | 3 | 17 | 65 | 0 |
| MLP_Model_2 | Wet | 28 | 24 | 23 | 2338 | 0 |
| MLP_Model_3 | Dry | 37 | 4 | 8 | 74 | 0 |
| MLP_Model_3 | Wet | 20 | 32 | 9 | 2352 | 1 |
| MLP_Model_4 | Dry | 39 | 2 | 19 | 63 | 1 |
| MLP_Model_4 | Wet | 26 | 26 | 20 | 2341 | 1 |
| Poisson | Dry | 40 | 1 | 14 | 68 | 0 |
| Poisson | Wet | 28 | 24 | 23 | 2338 | 1 |
| Tweedie | Dry | 38 | 3 | 15 | 67 | 0 |
| Tweedie | Wet | 27 | 25 | 18 | 2343 | 1 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 13 | 13 |
| Dry | MonthlyClimatology | 12 | 12 |
| Wet | Persistence | 13 | 12 |
| Wet | MonthlyClimatology | 13 | 13 |

### Sulawesi

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 4.354 | 1.592 | 0.338 | 5.292 | 9.573 |
| RandomForest | Wet | 0.512 | 0.290 | 0.054 | 3.211 | 3.431 |
| ExtraTrees | Dry | 4.265 | 1.579 | 0.365 | 5.145 | 9.311 |
| ExtraTrees | Wet | 0.513 | 0.292 | 0.051 | 3.244 | 3.498 |
| XGBoost | Dry | 4.263 | 1.626 | 0.365 | 5.337 | 9.187 |
| XGBoost | Wet | 0.501 | 0.255 | 0.093 | 3.198 | 3.337 |
| LightGBM | Dry | 4.251 | 1.653 | 0.369 | 5.275 | 9.117 |
| LightGBM | Wet | 0.514 | 0.301 | 0.048 | 3.152 | 3.293 |
| SVM_RBF | Dry | 4.424 | 1.641 | 0.316 | 5.858 | 9.750 |
| SVM_RBF | Wet | 0.526 | 0.221 | 0.000 | 3.423 | 3.676 |
| KNN | Dry | 4.663 | 1.726 | 0.241 | 5.923 | 10.161 |
| KNN | Wet | 0.561 | 0.360 | -0.136 | 3.493 | 3.756 |
| BayesianRidge | Dry | 4.156 | 1.561 | 0.397 | 5.254 | 9.137 |
| BayesianRidge | Wet | 0.515 | 0.252 | 0.042 | 3.173 | 3.433 |
| MLP_Model_1 | Dry | 4.144 | 1.538 | 0.400 | 5.248 | 9.094 |
| MLP_Model_1 | Wet | 0.549 | 0.251 | -0.087 | 3.347 | 3.606 |
| MLP_Model_2 | Dry | 4.383 | 1.632 | 0.329 | 5.466 | 9.219 |
| MLP_Model_2 | Wet | 0.551 | 0.274 | -0.096 | 3.420 | 3.633 |
| MLP_Model_3 | Dry | 4.394 | 1.646 | 0.326 | 5.481 | 9.414 |
| MLP_Model_3 | Wet | 0.535 | 0.296 | -0.034 | 3.272 | 3.423 |
| MLP_Model_4 | Dry | 4.595 | 1.666 | 0.262 | 5.663 | 9.292 |
| MLP_Model_4 | Wet | 0.518 | 0.165 | 0.031 | 3.395 | 3.512 |
| Poisson | Dry | 4.147 | 1.688 | 0.399 | 5.111 | 9.032 |
| Poisson | Wet | 0.517 | 0.282 | 0.037 | 3.309 | 3.568 |
| Tweedie | Dry | 4.342 | 1.620 | 0.341 | 5.460 | 9.619 |
| Tweedie | Wet | 0.508 | 0.230 | 0.069 | 3.454 | 3.702 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -0.234 | 157.091 | 0.484 | 0.235 | 0.422 |
| RandomForest | Wet | 0.109 | 194.892 | 0.000 | NA | 0.000 |
| ExtraTrees | Dry | -0.188 | 157.411 | 0.516 | 0.267 | 0.434 |
| ExtraTrees | Wet | 0.112 | 194.679 | 0.000 | NA | 0.000 |
| XGBoost | Dry | -0.008 | 156.977 | 0.539 | 0.266 | 0.451 |
| XGBoost | Wet | 0.073 | 194.621 | 0.000 | 1.000 | 0.000 |
| LightGBM | Dry | 0.065 | 156.903 | 0.555 | 0.268 | 0.461 |
| LightGBM | Wet | 0.126 | 194.229 | 0.000 | 1.000 | 0.000 |
| SVM_RBF | Dry | -0.666 | 131.673 | 0.383 | 0.319 | 0.325 |
| SVM_RBF | Wet | 0.021 | 137.017 | 0.000 | NA | 0.000 |
| KNN | Dry | -0.318 | 159.945 | 0.438 | 0.222 | 0.389 |
| KNN | Wet | 0.172 | 194.949 | 0.000 | NA | 0.000 |
| BayesianRidge | Dry | -0.237 | 151.445 | 0.531 | 0.261 | 0.447 |
| BayesianRidge | Wet | 0.075 | 171.868 | 0.000 | NA | 0.000 |
| MLP_Model_1 | Dry | -0.456 | 163.838 | 0.477 | 0.256 | 0.409 |
| MLP_Model_1 | Wet | 0.055 | 196.424 | 0.000 | 1.000 | 0.000 |
| MLP_Model_2 | Dry | -0.216 | 164.299 | 0.492 | 0.241 | 0.426 |
| MLP_Model_2 | Wet | 0.079 | 196.238 | 0.000 | NA | 0.000 |
| MLP_Model_3 | Dry | -0.221 | 160.926 | 0.477 | 0.291 | 0.399 |
| MLP_Model_3 | Wet | 0.112 | 195.205 | 0.000 | NA | 0.000 |
| MLP_Model_4 | Dry | 0.136 | 166.982 | 0.516 | 0.305 | 0.420 |
| MLP_Model_4 | Wet | -0.040 | 197.649 | 0.048 | 0.500 | 0.045 |
| Poisson | Dry | 0.044 | 154.266 | 0.578 | 0.282 | 0.471 |
| Poisson | Wet | 0.099 | 194.822 | 0.000 | NA | 0.000 |
| Tweedie | Dry | -0.291 | 157.287 | 0.492 | 0.250 | 0.423 |
| Tweedie | Wet | 0.034 | 196.018 | 0.000 | NA | 0.000 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 62 | 66 | 19 | 524 | 11 |
| RandomForest | Wet | 0 | 21 | 0 | 1844 | 0 |
| ExtraTrees | Dry | 66 | 62 | 24 | 519 | 12 |
| ExtraTrees | Wet | 0 | 21 | 0 | 1844 | 0 |
| XGBoost | Dry | 69 | 59 | 25 | 518 | 13 |
| XGBoost | Wet | 0 | 21 | 1 | 1843 | 0 |
| LightGBM | Dry | 71 | 57 | 26 | 517 | 14 |
| LightGBM | Wet | 0 | 21 | 1 | 1843 | 0 |
| SVM_RBF | Dry | 49 | 79 | 23 | 520 | 12 |
| SVM_RBF | Wet | 0 | 21 | 0 | 1844 | 0 |
| KNN | Dry | 56 | 72 | 16 | 527 | 9 |
| KNN | Wet | 0 | 21 | 0 | 1844 | 0 |
| BayesianRidge | Dry | 68 | 60 | 24 | 519 | 10 |
| BayesianRidge | Wet | 0 | 21 | 0 | 1844 | 0 |
| MLP_Model_1 | Dry | 61 | 67 | 21 | 522 | 12 |
| MLP_Model_1 | Wet | 0 | 21 | 1 | 1843 | 0 |
| MLP_Model_2 | Dry | 63 | 65 | 20 | 523 | 11 |
| MLP_Model_2 | Wet | 0 | 21 | 0 | 1844 | 0 |
| MLP_Model_3 | Dry | 61 | 67 | 25 | 518 | 13 |
| MLP_Model_3 | Wet | 0 | 21 | 0 | 1844 | 0 |
| MLP_Model_4 | Dry | 66 | 62 | 29 | 514 | 15 |
| MLP_Model_4 | Wet | 1 | 20 | 1 | 1843 | 1 |
| Poisson | Dry | 74 | 54 | 29 | 514 | 13 |
| Poisson | Wet | 0 | 21 | 0 | 1844 | 0 |
| Tweedie | Dry | 63 | 65 | 21 | 522 | 11 |
| Tweedie | Wet | 0 | 21 | 0 | 1844 | 0 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 13 | 13 |
| Dry | MonthlyClimatology | 13 | 13 |
| Wet | Persistence | 13 | 13 |
| Wet | MonthlyClimatology | 13 | 13 |

### Nusa Tenggara

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 3.539 | 1.398 | 0.443 | 7.056 | 10.279 |
| RandomForest | Wet | 0.223 | 0.110 | -0.068 | NA | NA |
| ExtraTrees | Dry | 3.506 | 1.373 | 0.453 | 6.859 | 10.150 |
| ExtraTrees | Wet | 0.218 | 0.091 | -0.018 | NA | NA |
| XGBoost | Dry | 3.727 | 1.377 | 0.382 | 7.455 | 10.897 |
| XGBoost | Wet | 0.218 | 0.038 | -0.024 | NA | NA |
| LightGBM | Dry | 3.699 | 1.374 | 0.391 | 7.432 | 10.802 |
| LightGBM | Wet | 0.220 | 0.037 | -0.034 | NA | NA |
| SVM_RBF | Dry | 4.472 | 1.674 | 0.110 | 9.162 | 12.920 |
| SVM_RBF | Wet | 0.236 | 0.071 | -0.199 | NA | NA |
| KNN | Dry | 3.952 | 1.594 | 0.305 | 7.910 | 11.446 |
| KNN | Wet | 0.289 | 0.226 | -0.787 | NA | NA |
| BayesianRidge | Dry | 3.465 | 1.362 | 0.466 | 6.769 | 9.853 |
| BayesianRidge | Wet | 0.231 | 0.085 | -0.147 | NA | NA |
| MLP_Model_1 | Dry | 4.079 | 1.563 | 0.260 | 7.985 | 11.398 |
| MLP_Model_1 | Wet | 0.218 | 0.031 | -0.021 | NA | NA |
| MLP_Model_2 | Dry | 4.159 | 1.555 | 0.230 | 8.571 | 12.111 |
| MLP_Model_2 | Wet | 0.216 | 0.029 | -0.005 | NA | NA |
| MLP_Model_3 | Dry | 3.949 | 1.674 | 0.306 | 7.495 | 11.168 |
| MLP_Model_3 | Wet | 0.326 | 0.280 | -1.280 | NA | NA |
| MLP_Model_4 | Dry | 4.116 | 1.691 | 0.246 | 7.286 | 11.055 |
| MLP_Model_4 | Wet | 0.217 | 0.031 | -0.013 | NA | NA |
| Poisson | Dry | 3.567 | 1.502 | 0.434 | 6.698 | 9.818 |
| Poisson | Wet | 0.222 | 0.101 | -0.054 | NA | NA |
| Tweedie | Dry | 3.624 | 1.471 | 0.416 | 6.988 | 9.995 |
| Tweedie | Wet | 0.214 | 0.050 | 0.014 | NA | NA |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -0.362 | 155.701 | 0.407 | 0.272 | 0.353 |
| RandomForest | Wet | 0.070 | 199.362 | NA | NA | NA |
| ExtraTrees | Dry | -0.348 | 156.057 | 0.431 | 0.285 | 0.368 |
| ExtraTrees | Wet | 0.049 | 199.550 | NA | NA | NA |
| XGBoost | Dry | -0.564 | 145.293 | 0.387 | 0.248 | 0.343 |
| XGBoost | Wet | -0.007 | 132.561 | NA | NA | NA |
| LightGBM | Dry | -0.566 | 147.777 | 0.377 | 0.260 | 0.333 |
| LightGBM | Wet | -0.008 | 143.774 | NA | NA | NA |
| SVM_RBF | Dry | -0.700 | 116.558 | 0.191 | 0.400 | 0.170 |
| SVM_RBF | Wet | 0.027 | 96.486 | NA | NA | NA |
| KNN | Dry | -0.380 | 156.840 | 0.294 | 0.355 | 0.253 |
| KNN | Wet | 0.186 | 199.276 | NA | NA | NA |
| BayesianRidge | Dry | -0.294 | 138.917 | 0.436 | 0.264 | 0.377 |
| BayesianRidge | Wet | 0.045 | 143.296 | NA | NA | NA |
| MLP_Model_1 | Dry | -0.428 | 164.237 | 0.353 | 0.385 | 0.289 |
| MLP_Model_1 | Wet | -0.014 | 199.959 | NA | NA | NA |
| MLP_Model_2 | Dry | -0.705 | 166.271 | 0.255 | 0.358 | 0.223 |
| MLP_Model_2 | Wet | -0.016 | 199.970 | NA | NA | NA |
| MLP_Model_3 | Dry | -0.193 | 158.225 | 0.392 | 0.398 | 0.311 |
| MLP_Model_3 | Wet | 0.242 | 199.075 | NA | NA | NA |
| MLP_Model_4 | Dry | -0.061 | 160.800 | 0.422 | 0.485 | 0.302 |
| MLP_Model_4 | Wet | -0.014 | 199.970 | NA | NA | NA |
| Poisson | Dry | 0.046 | 154.749 | 0.480 | 0.324 | 0.390 |
| Poisson | Wet | 0.059 | 199.564 | NA | NA | NA |
| Tweedie | Dry | -0.090 | 157.332 | 0.456 | 0.336 | 0.371 |
| Tweedie | Wet | 0.006 | 199.832 | NA | NA | NA |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 83 | 121 | 31 | 1728 | 2 |
| RandomForest | Wet | 0 | 0 | 0 | 573 | 0 |
| ExtraTrees | Dry | 88 | 116 | 35 | 1724 | 4 |
| ExtraTrees | Wet | 0 | 0 | 0 | 573 | 0 |
| XGBoost | Dry | 79 | 125 | 26 | 1733 | 3 |
| XGBoost | Wet | 0 | 0 | 0 | 573 | 0 |
| LightGBM | Dry | 77 | 127 | 27 | 1732 | 3 |
| LightGBM | Wet | 0 | 0 | 0 | 573 | 0 |
| SVM_RBF | Dry | 39 | 165 | 26 | 1733 | 5 |
| SVM_RBF | Wet | 0 | 0 | 0 | 573 | 0 |
| KNN | Dry | 60 | 144 | 33 | 1726 | 8 |
| KNN | Wet | 0 | 0 | 0 | 573 | 0 |
| BayesianRidge | Dry | 89 | 115 | 32 | 1727 | 2 |
| BayesianRidge | Wet | 0 | 0 | 0 | 573 | 0 |
| MLP_Model_1 | Dry | 72 | 132 | 45 | 1714 | 5 |
| MLP_Model_1 | Wet | 0 | 0 | 0 | 573 | 0 |
| MLP_Model_2 | Dry | 52 | 152 | 29 | 1730 | 4 |
| MLP_Model_2 | Wet | 0 | 0 | 0 | 573 | 0 |
| MLP_Model_3 | Dry | 80 | 124 | 53 | 1706 | 12 |
| MLP_Model_3 | Wet | 0 | 0 | 0 | 573 | 0 |
| MLP_Model_4 | Dry | 86 | 118 | 81 | 1678 | 15 |
| MLP_Model_4 | Wet | 0 | 0 | 0 | 573 | 0 |
| Poisson | Dry | 98 | 106 | 47 | 1712 | 6 |
| Poisson | Wet | 0 | 0 | 0 | 573 | 0 |
| Tweedie | Dry | 93 | 111 | 47 | 1712 | 4 |
| Tweedie | Wet | 0 | 0 | 0 | 573 | 0 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 13 | 13 |
| Dry | MonthlyClimatology | 13 | 7 |
| Wet | Persistence | 0 | 0 |
| Wet | MonthlyClimatology | 13 | 0 |

### Papua

| Model | State | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 14.504 | 6.482 | 0.152 | 11.054 | 21.685 |
| RandomForest | Wet | 3.071 | 1.030 | 0.158 | 7.614 | 15.215 |
| ExtraTrees | Dry | 14.530 | 6.570 | 0.149 | 11.001 | 21.615 |
| ExtraTrees | Wet | 3.061 | 1.052 | 0.164 | 7.552 | 15.099 |
| XGBoost | Dry | 13.991 | 6.612 | 0.211 | 11.531 | 20.820 |
| XGBoost | Wet | 2.957 | 0.934 | 0.220 | 7.425 | 14.568 |
| LightGBM | Dry | 14.061 | 6.478 | 0.203 | 11.403 | 20.979 |
| LightGBM | Wet | 2.938 | 0.903 | 0.230 | 7.498 | 14.542 |
| SVM_RBF | Dry | 15.743 | 6.287 | 0.001 | 12.803 | 23.924 |
| SVM_RBF | Wet | 3.339 | 0.635 | 0.005 | 9.216 | 16.974 |
| KNN | Dry | 14.804 | 6.844 | 0.116 | 11.235 | 21.872 |
| KNN | Wet | 3.128 | 1.294 | 0.127 | 7.534 | 14.844 |
| BayesianRidge | Dry | 14.785 | 6.054 | 0.118 | 11.637 | 22.401 |
| BayesianRidge | Wet | 2.950 | 0.784 | 0.223 | 7.667 | 14.748 |
| MLP_Model_1 | Dry | 14.814 | 7.899 | 0.115 | 12.324 | 21.420 |
| MLP_Model_1 | Wet | 3.797 | 2.176 | -0.287 | 7.423 | 15.657 |
| MLP_Model_2 | Dry | 14.312 | 6.051 | 0.174 | 11.742 | 21.498 |
| MLP_Model_2 | Wet | 3.179 | 0.610 | 0.098 | 8.560 | 16.057 |
| MLP_Model_3 | Dry | 13.895 | 6.458 | 0.221 | 11.433 | 20.582 |
| MLP_Model_3 | Wet | 3.234 | 1.191 | 0.067 | 7.831 | 15.501 |
| MLP_Model_4 | Dry | 14.688 | 5.718 | 0.130 | 11.992 | 22.373 |
| MLP_Model_4 | Wet | 3.251 | 0.593 | 0.057 | 8.752 | 16.571 |
| Poisson | Dry | 14.534 | 6.406 | 0.148 | 11.630 | 21.814 |
| Poisson | Wet | 2.946 | 0.695 | 0.225 | 7.639 | 14.716 |
| Tweedie | Dry | 14.886 | 6.539 | 0.106 | 11.852 | 22.326 |
| Tweedie | Wet | 2.956 | 0.625 | 0.220 | 7.873 | 14.802 |

| Model | State | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | -1.908 | 126.517 | 0.850 | 0.414 | 0.531 |
| RandomForest | Wet | 0.422 | 183.249 | 0.282 | 0.652 | 0.185 |
| ExtraTrees | Dry | -1.710 | 126.932 | 0.830 | 0.411 | 0.525 |
| ExtraTrees | Wet | 0.457 | 182.773 | 0.259 | 0.627 | 0.180 |
| XGBoost | Dry | -1.304 | 128.001 | 0.810 | 0.391 | 0.533 |
| XGBoost | Wet | 0.338 | 183.833 | 0.294 | 0.590 | 0.207 |
| LightGBM | Dry | -1.544 | 127.148 | 0.810 | 0.372 | 0.547 |
| LightGBM | Wet | 0.300 | 184.068 | 0.294 | 0.583 | 0.208 |
| SVM_RBF | Dry | -4.472 | 126.479 | 0.460 | 0.343 | 0.371 |
| SVM_RBF | Wet | -0.189 | 135.263 | 0.059 | 0.839 | 0.045 |
| KNN | Dry | -1.465 | 128.963 | 0.790 | 0.448 | 0.482 |
| KNN | Wet | 0.720 | 182.309 | 0.282 | 0.676 | 0.178 |
| BayesianRidge | Dry | -3.285 | 127.457 | 0.680 | 0.340 | 0.504 |
| BayesianRidge | Wet | 0.139 | 184.049 | 0.224 | 0.548 | 0.176 |
| MLP_Model_1 | Dry | 0.127 | 130.157 | 0.810 | 0.487 | 0.458 |
| MLP_Model_1 | Wet | 1.696 | 184.291 | 0.506 | 0.844 | 0.135 |
| MLP_Model_2 | Dry | -2.966 | 136.786 | 0.610 | 0.291 | 0.488 |
| MLP_Model_2 | Wet | -0.154 | 191.920 | 0.200 | 0.638 | 0.148 |
| MLP_Model_3 | Dry | -1.240 | 126.632 | 0.750 | 0.348 | 0.536 |
| MLP_Model_3 | Wet | 0.578 | 183.347 | 0.318 | 0.686 | 0.188 |
| MLP_Model_4 | Dry | -4.384 | 138.846 | 0.500 | 0.219 | 0.439 |
| MLP_Model_4 | Wet | -0.193 | 192.021 | 0.118 | 0.697 | 0.093 |
| Poisson | Dry | -2.224 | 127.681 | 0.750 | 0.375 | 0.517 |
| Poisson | Wet | 0.040 | 186.219 | 0.247 | 0.533 | 0.193 |
| Tweedie | Dry | -2.291 | 129.545 | 0.750 | 0.364 | 0.524 |
| Tweedie | Wet | -0.062 | 187.910 | 0.188 | 0.590 | 0.148 |

| Model | State | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| RandomForest | Dry | 85 | 15 | 60 | 74 | 27 |
| RandomForest | Wet | 24 | 61 | 45 | 2172 | 31 |
| ExtraTrees | Dry | 83 | 17 | 58 | 76 | 26 |
| ExtraTrees | Wet | 22 | 63 | 37 | 2180 | 26 |
| XGBoost | Dry | 81 | 19 | 52 | 82 | 25 |
| XGBoost | Wet | 25 | 60 | 36 | 2181 | 26 |
| LightGBM | Dry | 81 | 19 | 48 | 86 | 22 |
| LightGBM | Wet | 25 | 60 | 35 | 2182 | 25 |
| SVM_RBF | Dry | 46 | 54 | 24 | 110 | 12 |
| SVM_RBF | Wet | 5 | 80 | 26 | 2191 | 20 |
| KNN | Dry | 79 | 21 | 64 | 70 | 32 |
| KNN | Wet | 24 | 61 | 50 | 2167 | 34 |
| BayesianRidge | Dry | 68 | 32 | 35 | 99 | 15 |
| BayesianRidge | Wet | 19 | 66 | 23 | 2194 | 17 |
| MLP_Model_1 | Dry | 81 | 19 | 77 | 57 | 48 |
| MLP_Model_1 | Wet | 43 | 42 | 233 | 1984 | 171 |
| MLP_Model_2 | Dry | 61 | 39 | 25 | 109 | 12 |
| MLP_Model_2 | Wet | 17 | 68 | 30 | 2187 | 18 |
| MLP_Model_3 | Dry | 75 | 25 | 40 | 94 | 18 |
| MLP_Model_3 | Wet | 27 | 58 | 59 | 2158 | 39 |
| MLP_Model_4 | Dry | 50 | 50 | 14 | 120 | 7 |
| MLP_Model_4 | Wet | 10 | 75 | 23 | 2194 | 17 |
| Poisson | Dry | 75 | 25 | 45 | 89 | 22 |
| Poisson | Wet | 21 | 64 | 24 | 2193 | 17 |
| Tweedie | Dry | 75 | 25 | 43 | 91 | 18 |
| Tweedie | Wet | 16 | 69 | 23 | 2194 | 17 |

| State | Reference | Models with lower RMSE / 13 | Paired interval below zero / 13 |
| --- | --- | --- | --- |
| Dry | Persistence | 13 | 13 |
| Dry | MonthlyClimatology | 13 | 11 |
| Wet | Persistence | 13 | 12 |
| Wet | MonthlyClimatology | 12 | 9 |

## Reproducibility and disposition

- [Frozen season rule](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/season_definition.json>) and [published-source capture](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/sources/source_capture.json>).
- [Daily labels](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/daily_season_labels.csv>) and [year-specific intervals](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/season_intervals.csv>): explicit unit/date/rule/state mappings.
- [Frozen prediction source](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/aggregate_predictions.csv>): schedule=main, group=S5, partition=test.
- [Main metric source](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/primary_metrics.csv>): same scope; threshold retained by domain.
- [Audit evidence](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Seasonal_Evaluation_2026-10-11/audit_evidence.json>): source hashes and verification scope.

E02 rainfall-defined analysis and reviewer drafting are complete within the stated adaptation. Independent official zone-level season observations have not been validated. R3-A03 remains Partial pending coherent manuscript/form integration; it should be answered with this boundary explicitly stated. The original manuscript, notebook, model decisions and predictions are unchanged. No estimator fits or model inference were performed.
