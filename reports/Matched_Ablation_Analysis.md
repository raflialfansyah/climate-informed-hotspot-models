# Matched predictor-group ablation

Analyzed 11 October 2026. E01: Reviewer 2 major 4 and Reviewer 4 major 3.

**Local environmental predictors often add predictive value beyond hotspot history. Global climate indices add value inconsistently once local predictors are included. Neither finding is uniform across domains or metrics.**

These are comparisons of complete frozen prediction procedures. Each arm uses its own calibration factor and pre-test inversion choice under the same rule. Effects therefore include downstream recalibration and do not isolate a physical or causal effect of a predictor.

## Design and verification

| Group | Inputs | Columns |
| --- | --- | --- |
| S2 | Calendar + strictly lagged hotspot history | 26 |
| S3 | Calendar + local environment + global climate; no hotspot history | 59 |
| S4 | Calendar + hotspot history + local environment | 54 |
| S5 | Calendar + hotspot history + local environment + global climate | 81 |

Calendar controls are four month/day-of-year sine/cosine terms shared by every arm. The 22 history terms use observations through t-1. The 28 local terms include HTH, precipitation, evaporation, wind and rain summaries. The 27 global terms include SST-derived IOD/Nino and ROMI/amplitude features. Source provenance qualifications still apply; the ablation does not authenticate missing producer definitions.

BayesianRidge and MLP Model 2 were prespecified representatives, not selected from the test ranking. BayesianRidge uses seed 42; MLP uses seeds 42, 137 and 2026, with inverse-transformed count predictions averaged. Each arm uses the same candidate settings, schedules, domain support, 5,053 fit rows after common warmup and 2,557 scoring dates. MLP input width changes with group size, so the experiment holds the declared architecture/training rule rather than total parameter count fixed. Main fitting ends 2014; calibration is 2015-2016; inversion selection is 2017-2018; scoring is 2019-2025. No new fits, inversion decisions or test-based group choices were made.

All 56 arm tables were independently recomputed from saved dated predictions, including all 15 metrics. All 56 paired contrasts match dates, outcomes and training-derived thresholds. The 224 saved point/interval records and RMSE percentage-reduction intervals were independently reproduced. Supplementary intervals for RMSE90, bias, SMAPE, POD, FAR and CSI were calculated from the same saved predictions and paired year draws; original reports were preserved.

High activity means observed count >= the ceiling of the raw through-2014 training 90th percentile, before predictor warmup, fixed by domain across arms. MAE90/RMSE90 are errors on those observed high days. An event prediction is a predicted count meeting the same threshold. POD = hits/(hits+misses), FAR = false alarms/(hits+false alarms), CSI = hits/(hits+misses+false alarms). Zero-day false detections are predicted high events on observed-zero days. Bias is prediction minus observation; SMAPE is percent, with zero/zero contributing zero.

## Cross-domain pattern

Each entry counts improved point estimates out of 14 model/domain pairs. These counts are descriptive: domains overlap and two models share observations, so the 14 pairs are not independent replications. RMSE and R-squared on identical observations carry the same squared-error ranking.

| Contrast | RMSE | MAE | MAE90 | RMSE90 | POD | FAR | CSI | RMSE interval below zero |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S4 vs S2 | 10/14 | 8/14 | 10/14 | 12/14 | 12/14 | 8/14 | 12/14 | 8.0/14 |
| S5 vs S4 | 6/14 | 9/14 | 6/14 | 6/14 | 4/14 | 9/14 | 5/14 | 2.0/14 |
| S5 vs S2 | 10/14 | 12/14 | 8/14 | 10/14 | 10/14 | 11/14 | 11/14 | 6.0/14 |
| S5 vs S3 | 13/14 | 14/14 | 13/14 | 13/14 | 9/14 | 13/14 | 13/14 | 8.0/14 |

Lower error and FAR are favorable; higher POD/CSI are favorable. Ties do not count as improvement. Intervals are unadjusted 95% paired whole-year percentile intervals, 500 draws with seed 42 over seven years. They are conditional on fitted procedures, use few year blocks, retain within-year dependence but not dependence crossing year boundaries, and are not daily prediction intervals. An interval spanning zero is inconclusive. Multiple domains, models, contrasts and metrics are examined without multiplicity adjustment; intervals do not establish a definitive physical mechanism or independent confirmation on the already analyst-exposed test record.

## National example

| Model | Group | RMSE | MAE90 | RMSE90 | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 38.613 | 138.924 | 189.386 | 0.623 | 0.368 | 0.457 |
| BayesianRidge | S3 | 43.407 | 152.674 | 196.492 | 0.623 | 0.442 | 0.417 |
| BayesianRidge | S4 | 35.038 | 129.005 | 181.304 | 0.558 | 0.232 | 0.478 |
| BayesianRidge | S5 | 35.061 | 136.169 | 184.103 | 0.545 | 0.208 | 0.477 |
| MLP_Model_2 | S2 | 57.208 | 233.875 | 317.888 | 0.234 | 0.143 | 0.225 |
| MLP_Model_2 | S3 | 56.610 | 222.871 | 307.628 | 0.299 | 0.207 | 0.277 |
| MLP_Model_2 | S4 | 66.173 | 178.490 | 281.668 | 0.701 | 0.486 | 0.422 |
| MLP_Model_2 | S5 | 47.022 | 159.286 | 242.285 | 0.571 | 0.476 | 0.376 |

For national BayesianRidge, local predictors reduce RMSE by 9.3% (38.613 to 35.038), while adding global indices changes it to 35.061, with an interval spanning zero. For national MLP Model 2, local predictors worsen overall RMSE (57.208 to 66.173) even while improving MAE90/RMSE90. Adding global indices then reduces RMSE by 28.9% to 47.022, but POD falls from 0.701 to 0.571 and CSI from 0.422 to 0.376. Thus neither the national MLP result nor the cross-domain tally supports an unconditional climate-benefit claim.

## Important seed and fire-year exception

South Sumatra MLP Model 2 has a particularly large S4 error. The saved individual-seed RMSEs are 28.486, 316.954 and 25.921 for seeds 42, 137 and 2026; primary RMSE uses their averaged count predictions and is 109.013. All three S4 seeds selected plain inversion before test scoring, with effective factor 1. This exception therefore cannot be explained as a smearing correction applied to those predictions. Saved annual S4 RMSE is 279.946 in 2019 and 69.410 in 2023. Adding global indices reduces aggregate RMSE to 25.617, but that remains worse than S2 (23.639). The large S5-versus-S4 reduction is influenced by an unstable S4 seed and large fire-year errors, not evidence of a uniform global-climate benefit. Retain the prespecified seed averaging, disclose the exception, and do not drop the seed or alter inversion after seeing test performance. Finite predictions and an absence of recorded convergence warnings do not establish stable generalization.

## Paired effects in every domain

Difference = augmented minus reference; negative error/FAR differences favor the augmented arm. RMSE reduction = 100 x (reference RMSE - augmented RMSE)/reference RMSE, so positive percentages favor the augmented arm. Event-rate changes are fractions, not percentage-point numbers.

### S4 vs S2

| Domain | Model | RMSE difference | 95% interval | RMSE reduction % | MAE90 difference | RMSE90 difference | POD change | FAR change | CSI change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| National | BayesianRidge | -3.575 | [-5.327, -1.144] | 9.3 | -9.919 | -8.082 | -0.065 | -0.136 | 0.021 |
| National | MLP_Model_2 | 8.966 | [0.345, 33.301] | -15.7 | -55.385 | -36.220 | 0.468 | 0.343 | 0.197 |
| North Sumatra | BayesianRidge | -0.575 | [-0.959, -0.081] | 7.9 | -4.842 | -4.835 | 0.111 | 0.071 | 0.040 |
| North Sumatra | MLP_Model_2 | -1.272 | [-1.989, -0.342] | 14.0 | -8.456 | -7.254 | 0.089 | -0.203 | 0.082 |
| South Sumatra | BayesianRidge | -3.168 | [-5.551, -0.115] | 14.8 | -7.338 | -15.698 | 0.080 | 0.028 | 0.044 |
| South Sumatra | MLP_Model_2 | 85.373 | [-0.267, 145.543] | -361.2 | 200.511 | 391.961 | 0.188 | 0.123 | -0.000 |
| Kalimantan | BayesianRidge | 7.705 | [-2.330, 15.940] | -24.6 | 10.647 | 45.116 | 0.022 | -0.101 | 0.063 |
| Kalimantan | MLP_Model_2 | -13.218 | [-23.273, -0.344] | 29.9 | -49.592 | -73.767 | 0.419 | -0.096 | 0.277 |
| Sulawesi | BayesianRidge | -0.064 | [-0.125, -0.036] | 2.9 | 0.049 | -0.063 | -0.040 | -0.015 | -0.026 |
| Sulawesi | MLP_Model_2 | -0.272 | [-0.532, 0.064] | 11.2 | -0.650 | -1.855 | 0.181 | -0.021 | 0.119 |
| Nusa Tenggara | BayesianRidge | -0.084 | [-0.126, -0.041] | 2.7 | -0.204 | -0.277 | 0.025 | -0.039 | 0.028 |
| Nusa Tenggara | MLP_Model_2 | -0.156 | [-0.704, 0.517] | 4.4 | -1.680 | -2.147 | 0.289 | 0.050 | 0.140 |
| Papua | BayesianRidge | -0.056 | [-0.089, -0.034] | 1.0 | 0.061 | -0.003 | 0.016 | -0.083 | 0.039 |
| Papua | MLP_Model_2 | 0.007 | [-0.341, 0.299] | -0.1 | -1.109 | -1.261 | 0.211 | 0.011 | 0.079 |

### S5 vs S4

| Domain | Model | RMSE difference | 95% interval | RMSE reduction % | MAE90 difference | RMSE90 difference | POD change | FAR change | CSI change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| National | BayesianRidge | 0.023 | [-0.203, 0.510] | -0.1 | 7.164 | 2.799 | -0.013 | -0.025 | -0.001 |
| National | MLP_Model_2 | -19.151 | [-34.991, -4.293] | 28.9 | -19.205 | -39.383 | -0.130 | -0.010 | -0.046 |
| North Sumatra | BayesianRidge | -0.047 | [-0.085, 0.006] | 0.7 | 0.950 | 0.639 | 0.000 | -0.058 | 0.023 |
| North Sumatra | MLP_Model_2 | -0.042 | [-1.003, 1.515] | 0.5 | -5.546 | -6.646 | 0.156 | 0.131 | 0.061 |
| South Sumatra | BayesianRidge | 0.313 | [-0.010, 0.504] | -1.7 | 0.273 | 1.347 | 0.018 | 0.010 | 0.007 |
| South Sumatra | MLP_Model_2 | -83.395 | [-141.792, -0.460] | 76.5 | -191.554 | -380.579 | -0.473 | -0.297 | -0.148 |
| Kalimantan | BayesianRidge | 0.864 | [-0.214, 1.683] | -2.2 | 1.230 | 4.712 | 0.011 | -0.033 | 0.024 |
| Kalimantan | MLP_Model_2 | -2.379 | [-10.381, 8.406] | 7.7 | -4.784 | -27.610 | 0.000 | 0.024 | -0.015 |
| Sulawesi | BayesianRidge | 0.003 | [0.001, 0.006] | -0.2 | -0.011 | -0.017 | 0.020 | 0.008 | 0.013 |
| Sulawesi | MLP_Model_2 | 0.136 | [-0.054, 0.238] | -6.3 | 0.260 | 0.949 | -0.114 | -0.129 | -0.035 |
| Nusa Tenggara | BayesianRidge | 0.009 | [-0.003, 0.030] | -0.3 | 0.104 | 0.076 | -0.010 | -0.019 | -0.002 |
| Nusa Tenggara | MLP_Model_2 | 0.227 | [-0.541, 0.857] | -6.6 | 2.166 | 2.577 | -0.348 | -0.105 | -0.174 |
| Papua | BayesianRidge | -0.013 | [-0.026, 0.011] | 0.2 | -0.050 | -0.074 | 0.000 | 0.008 | -0.003 |
| Papua | MLP_Model_2 | 0.334 | [-0.270, 0.619] | -6.8 | 1.546 | 2.642 | -0.162 | -0.144 | -0.011 |

### S5 vs S2

| Domain | Model | RMSE difference | 95% interval | RMSE reduction % | MAE90 difference | RMSE90 difference | POD change | FAR change | CSI change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| National | BayesianRidge | -3.552 | [-5.385, -1.176] | 9.2 | -2.756 | -5.283 | -0.078 | -0.161 | 0.020 |
| National | MLP_Model_2 | -10.186 | [-18.703, 1.793] | 17.8 | -74.590 | -75.603 | 0.338 | 0.333 | 0.151 |
| North Sumatra | BayesianRidge | -0.623 | [-1.034, -0.135] | 8.6 | -3.893 | -4.196 | 0.111 | 0.013 | 0.063 |
| North Sumatra | MLP_Model_2 | -1.313 | [-2.761, 0.608] | 14.5 | -14.003 | -13.899 | 0.244 | -0.072 | 0.143 |
| South Sumatra | BayesianRidge | -2.856 | [-5.070, -0.116] | 13.3 | -7.065 | -14.352 | 0.098 | 0.038 | 0.050 |
| South Sumatra | MLP_Model_2 | 1.978 | [-0.982, 3.864] | -8.4 | 8.957 | 11.383 | -0.286 | -0.173 | -0.148 |
| Kalimantan | BayesianRidge | 8.569 | [-2.542, 17.623] | -27.4 | 11.877 | 49.828 | 0.032 | -0.134 | 0.087 |
| Kalimantan | MLP_Model_2 | -15.598 | [-33.788, 7.089] | 35.3 | -54.377 | -101.377 | 0.419 | -0.072 | 0.261 |
| Sulawesi | BayesianRidge | -0.061 | [-0.119, -0.033] | 2.7 | 0.038 | -0.079 | -0.020 | -0.007 | -0.013 |
| Sulawesi | MLP_Model_2 | -0.136 | [-0.319, 0.114] | 5.6 | -0.390 | -0.906 | 0.067 | -0.150 | 0.083 |
| Nusa Tenggara | BayesianRidge | -0.076 | [-0.124, -0.028] | 2.4 | -0.101 | -0.201 | 0.015 | -0.058 | 0.026 |
| Nusa Tenggara | MLP_Model_2 | 0.071 | [-0.075, 0.167] | -2.0 | 0.486 | 0.430 | -0.059 | -0.055 | -0.034 |
| Papua | BayesianRidge | -0.069 | [-0.114, -0.044] | 1.3 | 0.011 | -0.077 | 0.016 | -0.075 | 0.036 |
| Papua | MLP_Model_2 | 0.341 | [-0.099, 0.766] | -6.9 | 0.437 | 1.382 | 0.049 | -0.133 | 0.068 |

### S5 vs S3

| Domain | Model | RMSE difference | 95% interval | RMSE reduction % | MAE90 difference | RMSE90 difference | POD change | FAR change | CSI change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| National | BayesianRidge | -8.346 | [-15.069, -0.244] | 19.2 | -16.505 | -12.389 | -0.078 | -0.234 | 0.060 |
| National | MLP_Model_2 | -9.588 | [-17.134, 0.922] | 16.9 | -63.586 | -65.343 | 0.273 | 0.269 | 0.099 |
| North Sumatra | BayesianRidge | -2.616 | [-4.192, -0.580] | 28.2 | -16.744 | -17.912 | 0.467 | -0.504 | 0.348 |
| North Sumatra | MLP_Model_2 | -4.769 | [-7.844, -3.202] | 38.1 | -2.850 | -2.975 | 0.111 | -0.293 | 0.153 |
| South Sumatra | BayesianRidge | -3.602 | [-5.980, -0.484] | 16.2 | -2.202 | -15.389 | -0.116 | -0.189 | 0.066 |
| South Sumatra | MLP_Model_2 | 0.219 | [-1.126, 0.573] | -0.9 | 2.551 | 2.472 | -0.125 | -0.287 | -0.009 |
| Kalimantan | BayesianRidge | -7.721 | [-13.735, 0.382] | 16.2 | -28.701 | -38.448 | 0.075 | -0.135 | 0.112 |
| Kalimantan | MLP_Model_2 | -15.505 | [-30.726, 3.266] | 35.2 | -50.271 | -74.168 | -0.022 | -0.187 | 0.121 |
| Sulawesi | BayesianRidge | -0.355 | [-0.582, 0.023] | 14.0 | -0.858 | -1.402 | 0.054 | -0.157 | 0.081 |
| Sulawesi | MLP_Model_2 | -0.486 | [-0.882, 0.158] | 17.5 | -1.448 | -1.612 | 0.181 | -0.230 | 0.174 |
| Nusa Tenggara | BayesianRidge | -0.347 | [-0.484, -0.163] | 10.2 | -1.115 | -1.279 | 0.147 | -0.133 | 0.134 |
| Nusa Tenggara | MLP_Model_2 | -0.232 | [-0.354, -0.137] | 6.0 | -0.416 | -0.602 | 0.088 | -0.247 | 0.090 |
| Papua | BayesianRidge | -0.322 | [-0.525, -0.133] | 5.8 | -0.063 | -0.888 | -0.005 | -0.119 | 0.044 |
| Papua | MLP_Model_2 | -0.639 | [-1.237, -0.031] | 10.8 | -1.578 | -2.666 | 0.281 | -0.138 | 0.205 |

## Complete group metrics

All seven domains, both representatives and all four arms follow. Error/bias values are hotspot counts; SMAPE is percent; rates range from zero to one. Full precision is in the accompanying CSVs.

### National

Test days: 2557; event threshold: 156; observed high days: 77; zero days: 757.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 38.613 | 12.018 | 0.742 | 138.924 | 189.386 |
| BayesianRidge | S3 | 43.407 | 15.015 | 0.674 | 152.674 | 196.492 |
| BayesianRidge | S4 | 35.038 | 9.685 | 0.787 | 129.005 | 181.304 |
| BayesianRidge | S5 | 35.061 | 9.765 | 0.787 | 136.169 | 184.103 |
| MLP_Model_2 | S2 | 57.208 | 13.558 | 0.433 | 233.875 | 317.888 |
| MLP_Model_2 | S3 | 56.610 | 16.692 | 0.445 | 222.871 | 307.628 |
| MLP_Model_2 | S4 | 66.173 | 17.386 | 0.242 | 178.490 | 281.668 |
| MLP_Model_2 | S5 | 47.022 | 14.665 | 0.617 | 159.286 | 242.285 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 2.158 | 107.310 | 0.623 | 0.368 | 0.457 |
| BayesianRidge | S3 | 6.407 | 115.154 | 0.623 | 0.442 | 0.417 |
| BayesianRidge | S4 | -1.289 | 102.836 | 0.558 | 0.232 | 0.478 |
| BayesianRidge | S5 | -2.049 | 101.522 | 0.545 | 0.208 | 0.477 |
| MLP_Model_2 | S2 | -8.905 | 117.042 | 0.234 | 0.143 | 0.225 |
| MLP_Model_2 | S3 | -1.789 | 121.610 | 0.299 | 0.207 | 0.277 |
| MLP_Model_2 | S4 | 8.152 | 117.074 | 0.701 | 0.486 | 0.422 |
| MLP_Model_2 | S5 | 2.317 | 115.075 | 0.571 | 0.476 | 0.376 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 48 | 29 | 28 | 2452 | 0 |
| BayesianRidge | S3 | 48 | 29 | 38 | 2442 | 0 |
| BayesianRidge | S4 | 43 | 34 | 13 | 2467 | 0 |
| BayesianRidge | S5 | 42 | 35 | 11 | 2469 | 0 |
| MLP_Model_2 | S2 | 18 | 59 | 3 | 2477 | 0 |
| MLP_Model_2 | S3 | 23 | 54 | 6 | 2474 | 0 |
| MLP_Model_2 | S4 | 54 | 23 | 51 | 2429 | 0 |
| MLP_Model_2 | S5 | 44 | 33 | 40 | 2440 | 0 |

### North Sumatra

Test days: 2557; event threshold: 29; observed high days: 45; zero days: 1842.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 7.274 | 2.613 | 0.459 | 37.171 | 45.336 |
| BayesianRidge | S3 | 9.267 | 3.282 | 0.122 | 50.023 | 59.053 |
| BayesianRidge | S4 | 6.699 | 2.327 | 0.541 | 32.329 | 40.502 |
| BayesianRidge | S5 | 6.651 | 2.301 | 0.548 | 33.278 | 41.141 |
| MLP_Model_2 | S2 | 9.069 | 2.407 | 0.159 | 52.456 | 60.694 |
| MLP_Model_2 | S3 | 12.525 | 4.666 | -0.604 | 41.303 | 49.769 |
| MLP_Model_2 | S4 | 7.797 | 2.417 | 0.378 | 44.000 | 53.440 |
| MLP_Model_2 | S5 | 7.755 | 2.413 | 0.385 | 38.453 | 46.795 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 0.546 | 162.862 | 0.378 | 0.393 | 0.304 |
| BayesianRidge | S3 | 0.822 | 141.789 | 0.022 | 0.909 | 0.018 |
| BayesianRidge | S4 | 0.542 | 149.816 | 0.489 | 0.463 | 0.344 |
| BayesianRidge | S5 | 0.461 | 148.832 | 0.489 | 0.405 | 0.367 |
| MLP_Model_2 | S2 | -0.912 | 178.163 | 0.133 | 0.647 | 0.107 |
| MLP_Model_2 | S3 | 2.559 | 172.370 | 0.267 | 0.868 | 0.097 |
| MLP_Model_2 | S4 | -0.024 | 165.458 | 0.222 | 0.444 | 0.189 |
| MLP_Model_2 | S5 | 0.114 | 170.845 | 0.378 | 0.575 | 0.250 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 17 | 28 | 11 | 2501 | 0 |
| BayesianRidge | S3 | 1 | 44 | 10 | 2502 | 1 |
| BayesianRidge | S4 | 22 | 23 | 19 | 2493 | 0 |
| BayesianRidge | S5 | 22 | 23 | 15 | 2497 | 0 |
| MLP_Model_2 | S2 | 6 | 39 | 11 | 2501 | 1 |
| MLP_Model_2 | S3 | 12 | 33 | 79 | 2433 | 16 |
| MLP_Model_2 | S4 | 10 | 35 | 8 | 2504 | 0 |
| MLP_Model_2 | S5 | 17 | 28 | 23 | 2489 | 1 |

### South Sumatra

Test days: 2557; event threshold: 21; observed high days: 112; zero days: 1922.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 21.448 | 3.724 | 0.416 | 59.641 | 100.853 |
| BayesianRidge | S3 | 22.195 | 4.562 | 0.375 | 54.777 | 101.890 |
| BayesianRidge | S4 | 18.280 | 3.404 | 0.576 | 52.303 | 85.155 |
| BayesianRidge | S5 | 18.593 | 3.436 | 0.561 | 52.575 | 86.501 |
| MLP_Model_2 | S2 | 23.639 | 4.168 | 0.291 | 62.062 | 110.539 |
| MLP_Model_2 | S3 | 25.399 | 4.611 | 0.181 | 68.468 | 119.450 |
| MLP_Model_2 | S4 | 109.013 | 15.242 | -14.084 | 262.573 | 502.501 |
| MLP_Model_2 | S5 | 25.617 | 3.939 | 0.167 | 71.019 | 121.922 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | -1.878 | 149.935 | 0.589 | 0.214 | 0.508 |
| BayesianRidge | S3 | -0.299 | 144.353 | 0.804 | 0.441 | 0.492 |
| BayesianRidge | S4 | -1.017 | 128.779 | 0.670 | 0.242 | 0.551 |
| BayesianRidge | S5 | -0.999 | 129.233 | 0.688 | 0.252 | 0.558 |
| MLP_Model_2 | S2 | -1.691 | 179.542 | 0.652 | 0.336 | 0.490 |
| MLP_Model_2 | S3 | -1.903 | 177.721 | 0.491 | 0.450 | 0.350 |
| MLP_Model_2 | S4 | 13.726 | 179.860 | 0.839 | 0.460 | 0.490 |
| MLP_Model_2 | S5 | -3.176 | 181.790 | 0.366 | 0.163 | 0.342 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 66 | 46 | 18 | 2427 | 0 |
| BayesianRidge | S3 | 90 | 22 | 71 | 2374 | 9 |
| BayesianRidge | S4 | 75 | 37 | 24 | 2421 | 0 |
| BayesianRidge | S5 | 77 | 35 | 26 | 2419 | 0 |
| MLP_Model_2 | S2 | 73 | 39 | 37 | 2408 | 5 |
| MLP_Model_2 | S3 | 55 | 57 | 45 | 2400 | 6 |
| MLP_Model_2 | S4 | 94 | 18 | 80 | 2365 | 13 |
| MLP_Model_2 | S5 | 41 | 71 | 8 | 2437 | 0 |

### Kalimantan

Test days: 2557; event threshold: 51; observed high days: 93; zero days: 1643.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 31.325 | 7.572 | 0.610 | 110.785 | 155.127 |
| BayesianRidge | S3 | 47.615 | 8.956 | 0.098 | 151.363 | 243.403 |
| BayesianRidge | S4 | 39.030 | 7.191 | 0.394 | 121.432 | 200.243 |
| BayesianRidge | S5 | 39.894 | 7.234 | 0.367 | 122.662 | 204.955 |
| MLP_Model_2 | S2 | 44.140 | 8.460 | 0.225 | 149.913 | 226.361 |
| MLP_Model_2 | S3 | 44.048 | 11.418 | 0.228 | 145.808 | 199.152 |
| MLP_Model_2 | S4 | 30.922 | 7.551 | 0.620 | 100.321 | 152.594 |
| MLP_Model_2 | S5 | 28.543 | 7.534 | 0.676 | 95.537 | 124.984 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | -0.644 | 156.323 | 0.613 | 0.345 | 0.463 |
| BayesianRidge | S3 | 1.719 | 132.679 | 0.570 | 0.346 | 0.438 |
| BayesianRidge | S4 | 0.662 | 140.629 | 0.634 | 0.244 | 0.527 |
| BayesianRidge | S5 | 0.816 | 139.427 | 0.645 | 0.211 | 0.550 |
| MLP_Model_2 | S2 | -4.532 | 168.549 | 0.290 | 0.449 | 0.235 |
| MLP_Model_2 | S3 | 3.886 | 165.569 | 0.731 | 0.564 | 0.376 |
| MLP_Model_2 | S4 | -0.076 | 154.302 | 0.710 | 0.353 | 0.512 |
| MLP_Model_2 | S5 | 1.862 | 158.115 | 0.710 | 0.377 | 0.496 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 57 | 36 | 30 | 2434 | 0 |
| BayesianRidge | S3 | 53 | 40 | 28 | 2436 | 1 |
| BayesianRidge | S4 | 59 | 34 | 19 | 2445 | 0 |
| BayesianRidge | S5 | 60 | 33 | 16 | 2448 | 0 |
| MLP_Model_2 | S2 | 27 | 66 | 22 | 2442 | 2 |
| MLP_Model_2 | S3 | 68 | 25 | 88 | 2376 | 7 |
| MLP_Model_2 | S4 | 66 | 27 | 36 | 2428 | 1 |
| MLP_Model_2 | S5 | 66 | 27 | 40 | 2424 | 0 |

### Sulawesi

Test days: 2557; event threshold: 3; observed high days: 149; zero days: 2196.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 2.235 | 0.699 | 0.400 | 4.923 | 8.645 |
| BayesianRidge | S3 | 2.529 | 0.644 | 0.232 | 5.818 | 9.967 |
| BayesianRidge | S4 | 2.171 | 0.582 | 0.434 | 4.971 | 8.582 |
| BayesianRidge | S5 | 2.174 | 0.594 | 0.433 | 4.961 | 8.566 |
| MLP_Model_2 | S2 | 2.430 | 0.678 | 0.291 | 5.568 | 9.559 |
| MLP_Model_2 | S3 | 2.780 | 0.673 | 0.072 | 6.626 | 10.264 |
| MLP_Model_2 | S4 | 2.158 | 0.773 | 0.441 | 4.918 | 7.704 |
| MLP_Model_2 | S5 | 2.294 | 0.629 | 0.368 | 5.177 | 8.653 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 0.097 | 184.426 | 0.477 | 0.268 | 0.406 |
| BayesianRidge | S3 | -0.128 | 140.075 | 0.403 | 0.417 | 0.312 |
| BayesianRidge | S4 | -0.029 | 165.894 | 0.436 | 0.253 | 0.380 |
| BayesianRidge | S5 | -0.007 | 166.739 | 0.456 | 0.261 | 0.393 |
| MLP_Model_2 | S2 | -0.101 | 188.597 | 0.356 | 0.391 | 0.290 |
| MLP_Model_2 | S3 | -0.206 | 191.963 | 0.242 | 0.471 | 0.199 |
| MLP_Model_2 | S4 | 0.270 | 185.246 | 0.537 | 0.370 | 0.408 |
| MLP_Model_2 | S5 | 0.002 | 187.887 | 0.423 | 0.241 | 0.373 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 71 | 78 | 26 | 2382 | 11 |
| BayesianRidge | S3 | 60 | 89 | 43 | 2365 | 26 |
| BayesianRidge | S4 | 65 | 84 | 22 | 2386 | 10 |
| BayesianRidge | S5 | 68 | 81 | 24 | 2384 | 10 |
| MLP_Model_2 | S2 | 53 | 96 | 34 | 2374 | 23 |
| MLP_Model_2 | S3 | 36 | 113 | 32 | 2376 | 21 |
| MLP_Model_2 | S4 | 80 | 69 | 47 | 2361 | 24 |
| MLP_Model_2 | S5 | 63 | 86 | 20 | 2388 | 11 |

### Nusa Tenggara

Test days: 2557; event threshold: 6; observed high days: 204; zero days: 1871.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 3.114 | 1.134 | 0.456 | 6.870 | 10.055 |
| BayesianRidge | S3 | 3.385 | 1.219 | 0.358 | 7.884 | 11.133 |
| BayesianRidge | S4 | 3.030 | 1.080 | 0.485 | 6.665 | 9.778 |
| BayesianRidge | S5 | 3.038 | 1.065 | 0.483 | 6.769 | 9.853 |
| MLP_Model_2 | S2 | 3.575 | 1.252 | 0.283 | 8.085 | 11.681 |
| MLP_Model_2 | S3 | 3.878 | 1.318 | 0.157 | 8.986 | 12.713 |
| MLP_Model_2 | S4 | 3.419 | 1.319 | 0.345 | 6.405 | 9.534 |
| MLP_Model_2 | S5 | 3.646 | 1.200 | 0.255 | 8.571 | 12.111 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | -0.168 | 166.061 | 0.422 | 0.323 | 0.351 |
| BayesianRidge | S3 | -0.334 | 112.227 | 0.289 | 0.398 | 0.243 |
| BayesianRidge | S4 | -0.166 | 150.388 | 0.446 | 0.283 | 0.379 |
| BayesianRidge | S5 | -0.215 | 140.400 | 0.436 | 0.264 | 0.377 |
| MLP_Model_2 | S2 | -0.365 | 173.414 | 0.314 | 0.413 | 0.257 |
| MLP_Model_2 | S3 | -0.484 | 144.753 | 0.167 | 0.605 | 0.133 |
| MLP_Model_2 | S4 | 0.295 | 168.498 | 0.603 | 0.463 | 0.397 |
| MLP_Model_2 | S5 | -0.545 | 174.099 | 0.255 | 0.358 | 0.223 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 86 | 118 | 41 | 2312 | 6 |
| BayesianRidge | S3 | 59 | 145 | 39 | 2314 | 2 |
| BayesianRidge | S4 | 91 | 113 | 36 | 2317 | 3 |
| BayesianRidge | S5 | 89 | 115 | 32 | 2321 | 2 |
| MLP_Model_2 | S2 | 64 | 140 | 45 | 2308 | 8 |
| MLP_Model_2 | S3 | 34 | 170 | 52 | 2301 | 19 |
| MLP_Model_2 | S4 | 123 | 81 | 106 | 2247 | 22 |
| MLP_Model_2 | S5 | 52 | 152 | 29 | 2324 | 4 |

### Papua

Test days: 2557; event threshold: 3; observed high days: 185; zero days: 2132.

| Model | Group | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 5.345 | 1.422 | 0.212 | 9.802 | 19.343 |
| BayesianRidge | S3 | 5.599 | 1.803 | 0.135 | 9.876 | 20.154 |
| BayesianRidge | S4 | 5.290 | 1.249 | 0.228 | 9.863 | 19.340 |
| BayesianRidge | S5 | 5.277 | 1.263 | 0.232 | 9.813 | 19.266 |
| MLP_Model_2 | S2 | 4.936 | 1.125 | 0.328 | 9.843 | 17.809 |
| MLP_Model_2 | S3 | 5.916 | 1.118 | 0.034 | 11.858 | 21.857 |
| MLP_Model_2 | S4 | 4.943 | 2.035 | 0.326 | 8.734 | 16.548 |
| MLP_Model_2 | S5 | 5.277 | 1.103 | 0.232 | 10.280 | 19.191 |

| Model | Group | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 0.012 | 179.167 | 0.454 | 0.475 | 0.322 |
| BayesianRidge | S3 | 0.406 | 177.635 | 0.476 | 0.519 | 0.314 |
| BayesianRidge | S4 | -0.198 | 178.643 | 0.470 | 0.392 | 0.361 |
| BayesianRidge | S5 | -0.172 | 179.001 | 0.470 | 0.400 | 0.358 |
| MLP_Model_2 | S2 | -0.366 | 186.972 | 0.373 | 0.546 | 0.257 |
| MLP_Model_2 | S3 | -0.748 | 190.061 | 0.141 | 0.552 | 0.120 |
| MLP_Model_2 | S4 | 0.989 | 177.419 | 0.584 | 0.557 | 0.336 |
| MLP_Model_2 | S5 | -0.409 | 186.941 | 0.422 | 0.414 | 0.325 |

| Model | Group | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | S2 | 84 | 101 | 76 | 2296 | 42 |
| BayesianRidge | S3 | 88 | 97 | 95 | 2277 | 51 |
| BayesianRidge | S4 | 87 | 98 | 56 | 2316 | 31 |
| BayesianRidge | S5 | 87 | 98 | 58 | 2314 | 32 |
| MLP_Model_2 | S2 | 69 | 116 | 83 | 2289 | 46 |
| MLP_Model_2 | S3 | 26 | 159 | 32 | 2340 | 16 |
| MLP_Model_2 | S4 | 108 | 77 | 136 | 2236 | 84 |
| MLP_Model_2 | S5 | 78 | 107 | 55 | 2317 | 30 |

## Evidence and integration status

Analysis and shared response drafting are complete. The current manuscript and existing DOCX response forms still use the older procedure; these results must be integrated with the new main and temporal results under T07 before either reviewer comment is marked Done. Group ablation does not restore withdrawn individual-feature importance or ensemble claims.

- [Frozen primary arm metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/primary_metrics.csv>): schedule=main, partition=test, model in the two representatives.
- [Saved contrasts](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/ablation_contrasts.csv>): partition=test; augmented/reference/metric identify each row.
- [Saved dated predictions](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/aggregate_predictions.csv>): same filters plus unit/group/target_date.
- [Individual-seed metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/seed_metrics.csv>), [Annual metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/annual_metrics.csv>) and [Calibration decisions](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/calibration_diagnostics.csv>): schedule=main, unit=South Sumatra, model=MLP_Model_2, group=S4; test partition for metric tables, seed 137 for the high-error exception.
- [Workflow source](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Hotspot_SameDay_Lightweight/lightweight_workflow.py>): AB_GROUPS, AB_CONTRASTS, MAIN_SCHEDULE, run_light_ablation, create_light_reports.
- [Reviewer 2 major 4](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/reviewer_comments/Reviewer_2.md>) and [Reviewer 4 major 3](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/reviewer_comments/Reviewer_4.md>).
- [Audit evidence](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Matched_Ablation_Analysis_2026-10-11/audit_evidence.json>): source hashes, checked scope and source immutability.
