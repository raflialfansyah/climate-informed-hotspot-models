# Temporal robustness analysis

E03, 11 October 2026. Reviewer 1 major 6 and Reviewer 2 major 5.

**The additional temporal evaluations support frequent improvement over simple references, but performance is sensitive to domain, fire year and random seed. They do not establish uniform temporal robustness or stable model rankings.**

The three earlier schedules evaluate the full S5 predictor set for two prespecified representatives, BayesianRidge and MLP Model 2, in seven domains. Across the 42 earlier model/domain/window comparisons, point RMSE is lower than persistence in 39 and lower than monthly climatology in 41. National 2015-2016 is an important failure: both models lose to persistence, and MLP also loses to climatology. Negative R-squared values and seed instability are retained.

## Design and audit

| Schedule | Fit period | Calibration | Inversion selection | Evaluation | Fit rows | Scoring days |
| --- | --- | --- | --- | --- | --- | --- |
| fit_2008 | 2001-2008 | 2009-2010 | 2011-2012 | 2013-2014 | 2862 | 730 |
| fit_2010 | 2001-2010 | 2011-2012 | 2013-2014 | 2015-2016 | 3592 | 731 |
| fit_2012 | 2001-2012 | 2013-2014 | 2015-2016 | 2017-2018 | 4323 | 730 |
| main | 2001-2014 | 2015-2016 | 2017-2018 | 2019-2025 | 5053 | 2557 |

These are expanding fit-prefix temporal checks with two intervening two-year blocks for calibration and inversion selection. Estimators remain frozen during each evaluation window. They are not annually or daily retrained forecasts, and model fitting does not extend to the inversion-selection endpoint. The main scheme fits through 2014; 2015 is used for main calibration, not estimator fitting. The fit_2010 schedule evaluates 2015 without using that year in its own fitting, calibration or inversion-selection blocks.

Each S5 arm uses 81 prespecified columns with no numerical feature selector. Candidate settings, seeds and group membership are fixed across schedules; fitted preprocessing and SST anomaly references use the respective fitting prefix. The common 60-day warmup leaves 2,862/3,592/4,323/5,053 estimator-fit rows. BayesianRidge uses seed 42; MLP uses seeds 42, 137 and 2026 and averages count predictions after each seed applies its pre-evaluation inversion choice. Same-day environmental observations are assigned through t, and history through t-1. History uses realized prior observations within evaluation, so this is not a free-running multi-day forecast.

We authenticated all 36 report files and the 56 representative bundle/evaluation records. Independent reconstruction checked 840 primary metric values, 840 reference metric values, 1,680 individual-seed metric values, 2,730 annual metric values, seed averaging, complete dates, common outcomes and thresholds. All 336 saved representative absolute-interval records and 448 paired-reference records were independently reproduced. Added paired model comparisons and tail/event intervals are derived from saved predictions, without fitting or inference. Sources were hashed before and after and remained unchanged.

## Uncertainty and comparison rules

Intervals use 500 paired whole-year bootstrap draws, seed 42, with unadjusted 95% percentile limits conditional on fitted procedures. Each earlier window contains only two year blocks. Resampling two years twice gives only three distinct year compositions (first year twice, one of each, second year twice), so 500 draws do not create 500 independent years or a finely resolved interval. These intervals are coarse descriptive uncertainty summaries; seven main-evaluation year blocks are also few. Within-year dependence is retained, while dependence crossing year boundaries is not preserved. Training windows overlap and domains share observations, so fold/domain tallies are not independent replicates. No Diebold-Mariano test or all-13-model temporal comparison was performed.

Point errors and R-squared refer to different observed activity distributions across schedules. Do not read lower later RMSE as a measured improvement caused by additional training. Compare models/references only on matched dates within each window; the longer 2019-2025 window has a different duration. RMSE and R-squared share a squared-error ranking on identical observations. Skill here is 1 - model RMSE/reference RMSE; positive values favor the model.

Each domain/schedule freezes the ceiling of the raw fitting-period 90th count percentile before warmup. The threshold changes across schedules. MAE90/RMSE90 apply to observed counts meeting that threshold; POD, FAR and CSI use the same threshold for observed and predicted events. This is a training-relative high-activity definition, not a constant operational threshold across years. No-high-day errors and rates with zero denominators remain NA; they are not silently set to zero. Bootstrap intervals use finite resamples only and export their number, making sparse-event limitations visible.

## Reference skill across domains

| Evaluation | Model | Reference | Lower RMSE / 7 | RMSE interval below zero / 7 |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | Persistence | 7 | 7 |
| 2013-2014 | BayesianRidge | MonthlyClimatology | 7 | 6 |
| 2013-2014 | MLP_Model_2 | Persistence | 7 | 7 |
| 2013-2014 | MLP_Model_2 | MonthlyClimatology | 7 | 6 |
| 2015-2016 | BayesianRidge | Persistence | 6 | 6 |
| 2015-2016 | BayesianRidge | MonthlyClimatology | 7 | 7 |
| 2015-2016 | MLP_Model_2 | Persistence | 6 | 5 |
| 2015-2016 | MLP_Model_2 | MonthlyClimatology | 6 | 5 |
| 2017-2018 | BayesianRidge | Persistence | 7 | 7 |
| 2017-2018 | BayesianRidge | MonthlyClimatology | 7 | 7 |
| 2017-2018 | MLP_Model_2 | Persistence | 6 | 5 |
| 2017-2018 | MLP_Model_2 | MonthlyClimatology | 7 | 6 |
| 2019-2025 | BayesianRidge | Persistence | 7 | 7 |
| 2019-2025 | BayesianRidge | MonthlyClimatology | 7 | 7 |
| 2019-2025 | MLP_Model_2 | Persistence | 7 | 5 |
| 2019-2025 | MLP_Model_2 | MonthlyClimatology | 7 | 6 |

Earlier reference exceptions: National 2015-2016, both representatives versus persistence; National MLP versus climatology in the same window; South Sumatra MLP versus persistence in 2017-2018. The last exception has a paired RMSE interval wholly above zero. The national failure intervals span zero because performance differs sharply between 2015 and 2016, not because the adverse point results should be ignored.

## National example

| Evaluation | Model | RMSE | R-squared | MAE90 | RMSE90 | POD | FAR | CSI | RMSE skill vs persistence % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 109.894 | 0.375 | 197.528 | 308.507 | 0.437 | 0.255 | 0.380 | 22.8 |
| 2013-2014 | MLP_Model_2 | 119.214 | 0.265 | 227.677 | 335.865 | 0.287 | 0.324 | 0.253 | 16.2 |
| 2015-2016 | BayesianRidge | 145.342 | 0.336 | 311.010 | 425.518 | 0.910 | 0.184 | 0.755 | -13.9 |
| 2015-2016 | MLP_Model_2 | 284.986 | -1.553 | 643.018 | 834.599 | 0.962 | 0.359 | 0.625 | -123.3 |
| 2017-2018 | BayesianRidge | 22.402 | 0.673 | 105.978 | 123.332 | 0.385 | 0.375 | 0.312 | 35.0 |
| 2017-2018 | MLP_Model_2 | 31.453 | 0.356 | 73.190 | 88.854 | 0.769 | 0.565 | 0.385 | 8.8 |
| 2019-2025 | BayesianRidge | 35.061 | 0.787 | 136.169 | 184.103 | 0.545 | 0.208 | 0.477 | 37.4 |
| 2019-2025 | MLP_Model_2 | 47.022 | 0.617 | 159.286 | 242.285 | 0.571 | 0.476 | 0.376 | 16.1 |

In 2015-2016, national BayesianRidge RMSE is 145.342 versus MLP 284.986, with R-squared 0.336 and -1.553. Persistence RMSE is 127.605. For MLP, a high POD of 0.962 coexists with FAR 0.359, large count errors and worse reference skill. Threshold-event detection and accurate hotspot counts answer different questions.

The national MLP fit_2010 seed RMSEs are 191.356, 112.299 and 602.676 for seeds 42, 137 and 2026. All selected plain inversion with effective factor 1 before scoring. The primary average is retained, so its poor performance cannot be attributed to applying Duan smearing to those predictions. Annual MLP RMSE is 402.823 in 2015 versus 19.746 in 2016; predicted annual totals are 105,009 versus 44,891 observed in 2015. BayesianRidge also overestimates the 2015 total (65,149), though with lower error. This reveals fire-year and seed sensitivity despite finite saved outputs and the earlier warning audit.

National annual observed totals differ markedly: 44,891 in 2015, 5,348 in 2016, 2,518 in 2017 and 8,606 in 2018. In 2017 there are zero national high days under the fit_2012 threshold, so annual MAE90/RMSE90 are unavailable. The 2017-2018 national high-day results rest on only 13 observed high days, all in 2018. South Sumatra has only four high days in that window; its MLP R-squared is -1.476 and it loses to persistence. These qualifications prevent a uniformly robust extreme-event claim.

## Paired representative comparison

Difference = MLP Model 2 minus BayesianRidge. Negative error differences favor MLP. Point RMSE favors BayesianRidge in 5/7 domains in 2013-2014, 4/7 in 2015-2016, 6/7 in 2017-2018 and 6/7 in 2019-2025. This is a two-model comparison, not selection of the best of all 13 models. Intervals spanning zero are inconclusive; interval exclusions are unadjusted and based on few blocks.

| Domain | Evaluation | RMSE difference | 95% interval | RMSE90 difference | CSI difference |
| --- | --- | --- | --- | --- | --- |
| National | 2013-2014 | 9.320 | [6.203, 12.188] | 27.358 | -0.127 |
| National | 2015-2016 | 139.644 | [0.840, 198.010] | 409.081 | -0.130 |
| National | 2017-2018 | 9.051 | [1.362, 13.016] | -34.478 | 0.072 |
| National | 2019-2025 | 11.961 | [2.000, 21.107] | 58.182 | -0.101 |
| North Sumatra | 2013-2014 | -11.446 | [-30.034, 8.281] | -28.725 | -0.055 |
| North Sumatra | 2015-2016 | 1.316 | [0.527, 3.191] | -1.965 | 0.039 |
| North Sumatra | 2017-2018 | 0.461 | [0.176, 1.357] | -2.294 | -0.035 |
| North Sumatra | 2019-2025 | 1.104 | [0.434, 1.676] | 5.654 | -0.117 |
| South Sumatra | 2013-2014 | 5.734 | [1.589, 8.189] | 12.010 | -0.051 |
| South Sumatra | 2015-2016 | -3.998 | [-5.699, 0.813] | -11.791 | -0.007 |
| South Sumatra | 2017-2018 | 2.348 | [2.146, 2.622] | -3.313 | 0.062 |
| South Sumatra | 2019-2025 | 7.025 | [0.022, 12.249] | 35.421 | -0.216 |
| Kalimantan | 2013-2014 | 10.230 | [2.438, 14.896] | 36.904 | -0.115 |
| Kalimantan | 2015-2016 | -19.521 | [-27.789, -0.180] | -57.557 | -0.025 |
| Kalimantan | 2017-2018 | 3.493 | [3.463, 3.859] | 3.878 | 0.009 |
| Kalimantan | 2019-2025 | -11.351 | [-27.658, 9.095] | -79.971 | -0.054 |
| Sulawesi | 2013-2014 | -0.039 | [-0.096, -0.015] | -0.129 | -0.103 |
| Sulawesi | 2015-2016 | -0.278 | [-0.407, 0.102] | -0.947 | -0.031 |
| Sulawesi | 2017-2018 | -0.067 | [-0.233, 0.236] | -0.691 | 0.028 |
| Sulawesi | 2019-2025 | 0.120 | [0.050, 0.262] | 0.087 | -0.020 |
| Nusa Tenggara | 2013-2014 | 0.069 | [-0.011, 0.255] | -0.557 | -0.010 |
| Nusa Tenggara | 2015-2016 | 0.985 | [0.029, 1.434] | 4.486 | -0.375 |
| Nusa Tenggara | 2017-2018 | 0.375 | [0.161, 0.606] | -0.056 | -0.045 |
| Nusa Tenggara | 2019-2025 | 0.608 | [0.129, 1.010] | 2.257 | -0.154 |
| Papua | 2013-2014 | 0.075 | [-0.401, 0.237] | 0.308 | -0.042 |
| Papua | 2015-2016 | 3.443 | [1.808, 4.527] | 7.767 | -0.099 |
| Papua | 2017-2018 | 0.152 | [0.128, 0.261] | -0.241 | -0.081 |
| Papua | 2019-2025 | 0.000 | [-0.277, 0.392] | -0.076 | -0.033 |

## Figures

![RMSE skill relative to persistence](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Temporal_Robustness_Analysis_2026-10-11/temporal_persistence_skill.png>)

Positive percentages mean lower RMSE than persistence, within matched evaluation dates. Colors and labels are point estimates, without a significance claim. Thresholds, observation distributions and window duration differ across columns.

![National annual activity and error](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Temporal_Robustness_Analysis_2026-10-11/national_annual_diagnostics.png>)

Annual observations, frozen-procedure predicted totals and count RMSE use the procedure assigned to each evaluation year. Vertical boundaries separate the four schedules; lines do not represent one continuously updated fitted model. The 2015 MLP failure remains visible.

## Complete metrics by region and period

All 15 metrics follow, with absolute RMSE intervals and reference skill. Bias is predicted minus observed count. SMAPE is percent with zero/zero contributing zero. Rates range 0-1. Zero-day false detections count predicted high events on observed-zero days, not every positive predicted count. Full precision, other metric intervals and finite-resample counts are in the accompanying CSVs.

### National

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 163 | 87 | 90 | 46920 |
| 2015-2016 | 731 | 155 | 78 | 82 | 50239 |
| 2017-2018 | 730 | 153 | 13 | 188 | 11124 |
| 2019-2025 | 2557 | 156 | 77 | 757 | 50373 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 109.894 | 37.088 | 0.375 | 197.528 | 308.507 |
| 2013-2014 | MLP_Model_2 | 119.214 | 41.376 | 0.265 | 227.677 | 335.865 |
| 2015-2016 | BayesianRidge | 145.342 | 47.313 | 0.336 | 311.010 | 425.518 |
| 2015-2016 | MLP_Model_2 | 284.986 | 92.826 | -1.553 | 643.018 | 834.599 |
| 2017-2018 | BayesianRidge | 22.402 | 8.696 | 0.673 | 105.978 | 123.332 |
| 2017-2018 | MLP_Model_2 | 31.453 | 13.918 | 0.356 | 73.190 | 88.854 |
| 2019-2025 | BayesianRidge | 35.061 | 9.765 | 0.787 | 136.169 | 184.103 |
| 2019-2025 | MLP_Model_2 | 47.022 | 14.665 | 0.617 | 159.286 | 242.285 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -21.883 | 80.316 | 0.437 | 0.255 | 0.380 |
| 2013-2014 | MLP_Model_2 | -26.781 | 92.720 | 0.287 | 0.324 | 0.253 |
| 2015-2016 | BayesianRidge | 28.120 | 80.524 | 0.910 | 0.184 | 0.755 |
| 2015-2016 | MLP_Model_2 | 81.849 | 96.021 | 0.962 | 0.359 | 0.625 |
| 2017-2018 | BayesianRidge | -1.994 | 96.707 | 0.385 | 0.375 | 0.312 |
| 2017-2018 | MLP_Model_2 | 7.475 | 111.385 | 0.769 | 0.565 | 0.385 |
| 2019-2025 | BayesianRidge | -2.049 | 101.522 | 0.545 | 0.208 | 0.477 |
| 2019-2025 | MLP_Model_2 | 2.317 | 115.075 | 0.571 | 0.476 | 0.376 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 38 | 49 | 13 | 630 | 0 |
| 2013-2014 | MLP_Model_2 | 25 | 62 | 12 | 631 | 0 |
| 2015-2016 | BayesianRidge | 71 | 7 | 16 | 637 | 0 |
| 2015-2016 | MLP_Model_2 | 75 | 3 | 42 | 611 | 0 |
| 2017-2018 | BayesianRidge | 5 | 8 | 3 | 714 | 0 |
| 2017-2018 | MLP_Model_2 | 10 | 3 | 13 | 704 | 0 |
| 2019-2025 | BayesianRidge | 42 | 35 | 11 | 2469 | 0 |
| 2019-2025 | MLP_Model_2 | 44 | 33 | 40 | 2440 | 0 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [106.187, 113.481] | 22.8 | 21.1 |
| 2013-2014 | MLP_Model_2 | [112.390, 125.669] | 16.2 | 14.5 |
| 2015-2016 | BayesianRidge | [18.906, 204.813] | -13.9 | 9.3 |
| 2015-2016 | MLP_Model_2 | [19.746, 402.823] | -123.3 | -77.8 |
| 2017-2018 | BayesianRidge | [10.971, 29.721] | 35.0 | 65.7 |
| 2017-2018 | MLP_Model_2 | [12.333, 42.737] | 8.8 | 51.9 |
| 2019-2025 | BayesianRidge | [11.364, 55.410] | 37.4 | 59.4 |
| 2019-2025 | MLP_Model_2 | [13.306, 76.265] | 16.1 | 45.5 |

### North Sumatra

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 26 | 110 | 323 | 19847 |
| 2015-2016 | 731 | 27 | 55 | 334 | 5622 |
| 2017-2018 | 730 | 26 | 15 | 502 | 1829 |
| 2019-2025 | 2557 | 29 | 45 | 1842 | 5846 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 99.389 | 25.658 | 0.092 | 138.388 | 253.337 |
| 2013-2014 | MLP_Model_2 | 87.942 | 21.017 | 0.289 | 114.568 | 224.612 |
| 2015-2016 | BayesianRidge | 16.390 | 5.768 | 0.285 | 43.153 | 57.371 |
| 2015-2016 | MLP_Model_2 | 17.707 | 7.794 | 0.166 | 39.529 | 55.406 |
| 2017-2018 | BayesianRidge | 7.548 | 3.000 | 0.491 | 34.020 | 44.742 |
| 2017-2018 | MLP_Model_2 | 8.008 | 2.707 | 0.427 | 35.448 | 42.447 |
| 2019-2025 | BayesianRidge | 6.651 | 2.301 | 0.548 | 33.278 | 41.141 |
| 2019-2025 | MLP_Model_2 | 7.755 | 2.413 | 0.385 | 38.453 | 46.795 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 6.227 | 130.361 | 0.727 | 0.245 | 0.588 |
| 2013-2014 | MLP_Model_2 | -10.599 | 143.618 | 0.664 | 0.270 | 0.533 |
| 2015-2016 | BayesianRidge | -2.989 | 113.314 | 0.255 | 0.263 | 0.233 |
| 2015-2016 | MLP_Model_2 | 1.147 | 133.067 | 0.436 | 0.579 | 0.273 |
| 2017-2018 | BayesianRidge | 1.224 | 156.416 | 0.533 | 0.273 | 0.444 |
| 2017-2018 | MLP_Model_2 | 0.449 | 168.761 | 0.600 | 0.438 | 0.409 |
| 2019-2025 | BayesianRidge | 0.461 | 148.832 | 0.489 | 0.405 | 0.367 |
| 2019-2025 | MLP_Model_2 | 0.114 | 170.845 | 0.378 | 0.575 | 0.250 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 80 | 30 | 26 | 594 | 0 |
| 2013-2014 | MLP_Model_2 | 73 | 37 | 27 | 593 | 1 |
| 2015-2016 | BayesianRidge | 14 | 41 | 5 | 671 | 0 |
| 2015-2016 | MLP_Model_2 | 24 | 31 | 33 | 643 | 1 |
| 2017-2018 | BayesianRidge | 8 | 7 | 3 | 712 | 0 |
| 2017-2018 | MLP_Model_2 | 9 | 6 | 7 | 708 | 0 |
| 2019-2025 | BayesianRidge | 22 | 23 | 15 | 2497 | 0 |
| 2019-2025 | MLP_Model_2 | 17 | 28 | 23 | 2489 | 1 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [85.918, 111.240] | 11.4 | 4.0 |
| 2013-2014 | MLP_Model_2 | [81.206, 94.199] | 21.6 | 15.0 |
| 2015-2016 | BayesianRidge | [8.881, 21.422] | 23.4 | 19.4 |
| 2015-2016 | MLP_Model_2 | [12.073, 21.949] | 17.3 | 12.9 |
| 2017-2018 | BayesianRidge | [3.275, 10.159] | 22.0 | 48.8 |
| 2017-2018 | MLP_Model_2 | [4.632, 10.335] | 17.3 | 45.7 |
| 2019-2025 | BayesianRidge | [2.781, 10.181] | 37.7 | 63.3 |
| 2019-2025 | MLP_Model_2 | [3.270, 11.579] | 27.4 | 57.2 |

### South Sumatra

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 20 | 70 | 429 | 5831 |
| 2015-2016 | 731 | 19 | 83 | 458 | 10580 |
| 2017-2018 | 730 | 21 | 4 | 546 | 739 |
| 2019-2025 | 2557 | 21 | 112 | 1922 | 12008 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 17.097 | 5.782 | 0.495 | 37.860 | 53.298 |
| 2013-2014 | MLP_Model_2 | 22.831 | 7.340 | 0.099 | 45.676 | 65.308 |
| 2015-2016 | BayesianRidge | 39.271 | 10.081 | 0.458 | 70.380 | 114.549 |
| 2015-2016 | MLP_Model_2 | 35.273 | 9.618 | 0.562 | 63.239 | 102.758 |
| 2017-2018 | BayesianRidge | 2.589 | 1.020 | 0.319 | 23.261 | 23.812 |
| 2017-2018 | MLP_Model_2 | 4.937 | 2.287 | -1.476 | 19.515 | 20.498 |
| 2019-2025 | BayesianRidge | 18.593 | 3.436 | 0.561 | 52.575 | 86.501 |
| 2019-2025 | MLP_Model_2 | 25.617 | 3.939 | 0.167 | 71.019 | 121.922 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -1.800 | 146.106 | 0.614 | 0.218 | 0.524 |
| 2013-2014 | MLP_Model_2 | 0.177 | 158.305 | 0.629 | 0.343 | 0.473 |
| 2015-2016 | BayesianRidge | 2.032 | 148.872 | 0.867 | 0.163 | 0.742 |
| 2015-2016 | MLP_Model_2 | -1.437 | 149.963 | 0.904 | 0.202 | 0.735 |
| 2017-2018 | BayesianRidge | -0.106 | 121.564 | 0.000 | NA | 0.000 |
| 2017-2018 | MLP_Model_2 | 1.602 | 167.585 | 0.250 | 0.923 | 0.062 |
| 2019-2025 | BayesianRidge | -0.999 | 129.233 | 0.688 | 0.252 | 0.558 |
| 2019-2025 | MLP_Model_2 | -3.176 | 181.790 | 0.366 | 0.163 | 0.342 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 43 | 27 | 12 | 648 | 2 |
| 2013-2014 | MLP_Model_2 | 44 | 26 | 23 | 637 | 3 |
| 2015-2016 | BayesianRidge | 72 | 11 | 14 | 634 | 0 |
| 2015-2016 | MLP_Model_2 | 75 | 8 | 19 | 629 | 1 |
| 2017-2018 | BayesianRidge | 0 | 4 | 0 | 726 | 0 |
| 2017-2018 | MLP_Model_2 | 1 | 3 | 12 | 714 | 2 |
| 2019-2025 | BayesianRidge | 77 | 35 | 26 | 2419 | 0 |
| 2019-2025 | MLP_Model_2 | 41 | 71 | 8 | 2437 | 0 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [10.868, 21.599] | 34.3 | 27.8 |
| 2013-2014 | MLP_Model_2 | [12.457, 29.788] | 12.2 | 3.5 |
| 2015-2016 | BayesianRidge | [1.865, 55.544] | 30.9 | 21.6 |
| 2015-2016 | MLP_Model_2 | [2.678, 49.846] | 37.9 | 29.5 |
| 2017-2018 | BayesianRidge | [1.456, 3.359] | 39.2 | 83.3 |
| 2017-2018 | MLP_Model_2 | [3.602, 5.981] | -16.0 | 68.1 |
| 2019-2025 | BayesianRidge | [2.137, 31.125] | 33.2 | 34.2 |
| 2019-2025 | MLP_Model_2 | [2.221, 43.357] | 8.0 | 9.4 |

### Kalimantan

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 57 | 75 | 279 | 16425 |
| 2015-2016 | 731 | 50 | 85 | 314 | 24633 |
| 2017-2018 | 730 | 49 | 26 | 480 | 5045 |
| 2019-2025 | 2557 | 51 | 93 | 1643 | 23440 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 46.002 | 14.582 | 0.520 | 84.346 | 135.837 |
| 2013-2014 | MLP_Model_2 | 56.232 | 16.388 | 0.283 | 116.510 | 172.741 |
| 2015-2016 | BayesianRidge | 101.720 | 26.581 | 0.254 | 185.454 | 291.658 |
| 2015-2016 | MLP_Model_2 | 82.199 | 23.978 | 0.513 | 159.793 | 234.101 |
| 2017-2018 | BayesianRidge | 15.026 | 4.311 | 0.711 | 59.670 | 72.057 |
| 2017-2018 | MLP_Model_2 | 18.519 | 6.682 | 0.561 | 58.326 | 75.936 |
| 2019-2025 | BayesianRidge | 39.894 | 7.234 | 0.367 | 122.662 | 204.955 |
| 2019-2025 | MLP_Model_2 | 28.543 | 7.534 | 0.676 | 95.537 | 124.984 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -2.927 | 119.770 | 0.653 | 0.300 | 0.510 |
| 2013-2014 | MLP_Model_2 | -10.591 | 125.267 | 0.453 | 0.244 | 0.395 |
| 2015-2016 | BayesianRidge | 8.822 | 120.188 | 0.871 | 0.178 | 0.733 |
| 2015-2016 | MLP_Model_2 | 6.716 | 127.490 | 0.882 | 0.219 | 0.708 |
| 2017-2018 | BayesianRidge | -2.084 | 118.913 | 0.500 | 0.133 | 0.464 |
| 2017-2018 | MLP_Model_2 | 1.772 | 157.978 | 0.692 | 0.400 | 0.474 |
| 2019-2025 | BayesianRidge | 0.816 | 139.427 | 0.645 | 0.211 | 0.550 |
| 2019-2025 | MLP_Model_2 | 1.862 | 158.115 | 0.710 | 0.377 | 0.496 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 49 | 26 | 21 | 634 | 0 |
| 2013-2014 | MLP_Model_2 | 34 | 41 | 11 | 644 | 0 |
| 2015-2016 | BayesianRidge | 74 | 11 | 16 | 630 | 0 |
| 2015-2016 | MLP_Model_2 | 75 | 10 | 21 | 625 | 0 |
| 2017-2018 | BayesianRidge | 13 | 13 | 2 | 702 | 0 |
| 2017-2018 | MLP_Model_2 | 18 | 8 | 12 | 692 | 0 |
| 2019-2025 | BayesianRidge | 60 | 33 | 16 | 2448 | 0 |
| 2019-2025 | MLP_Model_2 | 66 | 27 | 40 | 2424 | 0 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [30.197, 57.624] | 44.8 | 31.4 |
| 2013-2014 | MLP_Model_2 | [32.635, 72.520] | 32.6 | 16.2 |
| 2015-2016 | BayesianRidge | [14.912, 143.176] | 23.5 | 6.2 |
| 2015-2016 | MLP_Model_2 | [14.732, 115.387] | 38.1 | 24.2 |
| 2017-2018 | BayesianRidge | [8.034, 19.672] | 52.1 | 64.2 |
| 2017-2018 | MLP_Model_2 | [11.497, 23.531] | 41.0 | 55.9 |
| 2019-2025 | BayesianRidge | [10.320, 65.921] | 25.0 | 28.4 |
| 2019-2025 | MLP_Model_2 | [13.096, 40.995] | 46.4 | 48.8 |

### Sulawesi

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 5 | 62 | 578 | 1082 |
| 2015-2016 | 731 | 4 | 87 | 535 | 2008 |
| 2017-2018 | 730 | 3 | 58 | 591 | 545 |
| 2019-2025 | 2557 | 3 | 149 | 2196 | 1490 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 3.742 | 1.125 | 0.535 | 7.915 | 12.493 |
| 2013-2014 | MLP_Model_2 | 3.703 | 1.033 | 0.545 | 8.393 | 12.364 |
| 2015-2016 | BayesianRidge | 8.285 | 1.934 | 0.572 | 11.883 | 23.785 |
| 2015-2016 | MLP_Model_2 | 8.007 | 1.908 | 0.600 | 11.816 | 22.839 |
| 2017-2018 | BayesianRidge | 2.079 | 0.773 | 0.418 | 5.065 | 6.980 |
| 2017-2018 | MLP_Model_2 | 2.011 | 0.761 | 0.455 | 4.752 | 6.290 |
| 2019-2025 | BayesianRidge | 2.174 | 0.594 | 0.433 | 4.961 | 8.566 |
| 2019-2025 | MLP_Model_2 | 2.294 | 0.629 | 0.368 | 5.177 | 8.653 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -0.232 | 158.120 | 0.597 | 0.119 | 0.552 |
| 2013-2014 | MLP_Model_2 | -0.553 | 183.233 | 0.500 | 0.184 | 0.449 |
| 2015-2016 | BayesianRidge | -0.161 | 156.046 | 0.747 | 0.207 | 0.625 |
| 2015-2016 | MLP_Model_2 | -0.471 | 171.946 | 0.655 | 0.136 | 0.594 |
| 2017-2018 | BayesianRidge | -0.085 | 163.790 | 0.379 | 0.312 | 0.324 |
| 2017-2018 | MLP_Model_2 | 0.003 | 182.017 | 0.448 | 0.381 | 0.351 |
| 2019-2025 | BayesianRidge | -0.007 | 166.739 | 0.456 | 0.261 | 0.393 |
| 2019-2025 | MLP_Model_2 | 0.002 | 187.887 | 0.423 | 0.241 | 0.373 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 37 | 25 | 5 | 663 | 0 |
| 2013-2014 | MLP_Model_2 | 31 | 31 | 7 | 661 | 1 |
| 2015-2016 | BayesianRidge | 65 | 22 | 17 | 627 | 4 |
| 2015-2016 | MLP_Model_2 | 57 | 30 | 9 | 635 | 2 |
| 2017-2018 | BayesianRidge | 22 | 36 | 10 | 662 | 4 |
| 2017-2018 | MLP_Model_2 | 26 | 32 | 16 | 656 | 8 |
| 2019-2025 | BayesianRidge | 68 | 81 | 24 | 2384 | 10 |
| 2019-2025 | MLP_Model_2 | 63 | 86 | 20 | 2388 | 11 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [2.346, 4.744] | 47.7 | 24.2 |
| 2013-2014 | MLP_Model_2 | [2.250, 4.729] | 48.3 | 25.0 |
| 2015-2016 | BayesianRidge | [1.201, 11.663] | 46.4 | 30.4 |
| 2015-2016 | MLP_Model_2 | [1.303, 11.256] | 48.2 | 32.7 |
| 2017-2018 | BayesianRidge | [1.235, 2.668] | 46.4 | 35.1 |
| 2017-2018 | MLP_Model_2 | [1.471, 2.434] | 48.1 | 37.2 |
| 2019-2025 | BayesianRidge | [0.707, 3.428] | 42.2 | 37.0 |
| 2019-2025 | MLP_Model_2 | [0.825, 3.536] | 39.0 | 33.6 |

### Nusa Tenggara

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 8 | 53 | 528 | 1322 |
| 2015-2016 | 731 | 7 | 48 | 542 | 1054 |
| 2017-2018 | 730 | 6 | 66 | 506 | 1191 |
| 2019-2025 | 2557 | 6 | 204 | 1871 | 3588 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 3.681 | 1.281 | 0.502 | 9.185 | 12.709 |
| 2013-2014 | MLP_Model_2 | 3.750 | 1.316 | 0.484 | 8.871 | 12.153 |
| 2015-2016 | BayesianRidge | 2.950 | 1.057 | 0.551 | 6.849 | 10.353 |
| 2015-2016 | MLP_Model_2 | 3.935 | 1.345 | 0.201 | 11.442 | 14.839 |
| 2017-2018 | BayesianRidge | 2.666 | 1.141 | 0.548 | 6.642 | 7.983 |
| 2017-2018 | MLP_Model_2 | 3.041 | 1.575 | 0.412 | 6.502 | 7.927 |
| 2019-2025 | BayesianRidge | 3.038 | 1.065 | 0.483 | 6.769 | 9.853 |
| 2019-2025 | MLP_Model_2 | 3.646 | 1.200 | 0.255 | 8.571 | 12.111 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -0.247 | 137.478 | 0.453 | 0.385 | 0.353 |
| 2013-2014 | MLP_Model_2 | -0.171 | 168.518 | 0.472 | 0.444 | 0.342 |
| 2015-2016 | BayesianRidge | 0.118 | 159.659 | 0.646 | 0.311 | 0.500 |
| 2015-2016 | MLP_Model_2 | -0.597 | 170.429 | 0.125 | 0.000 | 0.125 |
| 2017-2018 | BayesianRidge | -0.299 | 117.991 | 0.515 | 0.320 | 0.415 |
| 2017-2018 | MLP_Model_2 | 0.264 | 161.207 | 0.561 | 0.479 | 0.370 |
| 2019-2025 | BayesianRidge | -0.215 | 140.400 | 0.436 | 0.264 | 0.377 |
| 2019-2025 | MLP_Model_2 | -0.545 | 174.099 | 0.255 | 0.358 | 0.223 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 24 | 29 | 15 | 662 | 0 |
| 2013-2014 | MLP_Model_2 | 25 | 28 | 20 | 657 | 0 |
| 2015-2016 | BayesianRidge | 31 | 17 | 14 | 669 | 1 |
| 2015-2016 | MLP_Model_2 | 6 | 42 | 0 | 683 | 0 |
| 2017-2018 | BayesianRidge | 34 | 32 | 16 | 648 | 2 |
| 2017-2018 | MLP_Model_2 | 37 | 29 | 34 | 630 | 6 |
| 2019-2025 | BayesianRidge | 89 | 115 | 32 | 2321 | 2 |
| 2019-2025 | MLP_Model_2 | 52 | 152 | 29 | 2324 | 4 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [2.079, 4.773] | 40.8 | 17.9 |
| 2013-2014 | MLP_Model_2 | [2.334, 4.762] | 39.7 | 16.4 |
| 2015-2016 | BayesianRidge | [1.212, 3.995] | 41.8 | 27.6 |
| 2015-2016 | MLP_Model_2 | [1.240, 5.429] | 22.4 | 3.5 |
| 2017-2018 | BayesianRidge | [2.449, 2.867] | 42.6 | 19.9 |
| 2017-2018 | MLP_Model_2 | [3.028, 3.055] | 34.5 | 8.6 |
| 2019-2025 | BayesianRidge | [1.878, 4.226] | 34.6 | 23.0 |
| 2019-2025 | MLP_Model_2 | [2.092, 5.233] | 21.5 | 7.6 |

### Papua

| Evaluation | Days | Training threshold | Observed high days | Zero days | Observed total |
| --- | --- | --- | --- | --- | --- |
| 2013-2014 | 730 | 3 | 118 | 544 | 1944 |
| 2015-2016 | 731 | 3 | 145 | 534 | 4894 |
| 2017-2018 | 730 | 3 | 88 | 569 | 1400 |
| 2019-2025 | 2557 | 3 | 185 | 2132 | 2714 |

| Evaluation | Model | RMSE | MAE | R-squared | MAE90 | RMSE90 |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 8.497 | 2.501 | 0.284 | 11.613 | 20.845 |
| 2013-2014 | MLP_Model_2 | 8.573 | 2.191 | 0.271 | 11.707 | 21.153 |
| 2015-2016 | BayesianRidge | 16.774 | 5.009 | 0.490 | 22.236 | 37.512 |
| 2015-2016 | MLP_Model_2 | 20.218 | 5.827 | 0.259 | 26.781 | 45.279 |
| 2017-2018 | BayesianRidge | 7.835 | 1.964 | 0.228 | 10.624 | 22.298 |
| 2017-2018 | MLP_Model_2 | 7.987 | 2.411 | 0.198 | 10.960 | 22.056 |
| 2019-2025 | BayesianRidge | 5.277 | 1.263 | 0.232 | 9.813 | 19.266 |
| 2019-2025 | MLP_Model_2 | 5.277 | 1.103 | 0.232 | 10.280 | 19.191 |

| Evaluation | Model | Bias | SMAPE % | POD | FAR | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | -1.049 | 168.125 | 0.602 | 0.311 | 0.473 |
| 2013-2014 | MLP_Model_2 | -1.486 | 180.308 | 0.508 | 0.259 | 0.432 |
| 2015-2016 | BayesianRidge | -2.005 | 163.523 | 0.814 | 0.192 | 0.682 |
| 2015-2016 | MLP_Model_2 | -0.810 | 172.682 | 0.676 | 0.190 | 0.583 |
| 2017-2018 | BayesianRidge | -0.580 | 172.311 | 0.568 | 0.375 | 0.424 |
| 2017-2018 | MLP_Model_2 | 0.055 | 173.839 | 0.568 | 0.537 | 0.342 |
| 2019-2025 | BayesianRidge | -0.172 | 179.001 | 0.470 | 0.400 | 0.358 |
| 2019-2025 | MLP_Model_2 | -0.409 | 186.941 | 0.422 | 0.414 | 0.325 |

| Evaluation | Model | Hits | Misses | False alarms | Correct negatives | Zero-day false detections |
| --- | --- | --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | 71 | 47 | 32 | 580 | 14 |
| 2013-2014 | MLP_Model_2 | 60 | 58 | 21 | 591 | 10 |
| 2015-2016 | BayesianRidge | 118 | 27 | 28 | 558 | 15 |
| 2015-2016 | MLP_Model_2 | 98 | 47 | 23 | 563 | 10 |
| 2017-2018 | BayesianRidge | 50 | 38 | 30 | 612 | 18 |
| 2017-2018 | MLP_Model_2 | 50 | 38 | 58 | 584 | 37 |
| 2019-2025 | BayesianRidge | 87 | 98 | 58 | 2314 | 32 |
| 2019-2025 | MLP_Model_2 | 78 | 107 | 55 | 2317 | 30 |

| Evaluation | Model | RMSE 95% interval | RMSE skill vs persistence % | RMSE skill vs climatology % |
| --- | --- | --- | --- | --- |
| 2013-2014 | BayesianRidge | [3.788, 11.404] | 28.3 | 8.5 |
| 2013-2014 | MLP_Model_2 | [3.387, 11.641] | 27.7 | 7.7 |
| 2015-2016 | BayesianRidge | [7.940, 22.368] | 32.2 | 28.1 |
| 2015-2016 | MLP_Model_2 | [9.748, 26.895] | 18.3 | 13.4 |
| 2017-2018 | BayesianRidge | [3.976, 10.342] | 27.2 | 7.3 |
| 2017-2018 | MLP_Model_2 | [4.237, 10.470] | 25.8 | 5.5 |
| 2019-2025 | BayesianRidge | [1.857, 7.679] | 29.7 | 11.3 |
| 2019-2025 | MLP_Model_2 | [1.869, 7.571] | 29.7 | 11.3 |

## Disposition and source locators

E03 analysis and shared reviewer response drafting are complete. Manuscript and existing DOCX forms are not integrated. Reviewer 1 major 6 remains Partial because coherent new-lineage integration and broader main-model comparison reporting remain under T07. Reviewer 2 major 5 also remains Partial until integration. The evidence addresses the requested additional temporal evaluation within the declared two-model scope, without claiming independence, universal robustness or operational early warning.

The already analyst-exposed retrospective record was not used here to change hyperparameters, predictor groups, seed averaging or inversion. Missing producer definitions remain unresolved; this analysis checks the saved implementation and predictions, not original satellite/meteorological source authenticity. Neither the original manuscript nor notebook/model/prediction artifacts were changed.

- [Primary metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/primary_metrics.csv>): group=S5; model=BayesianRidge/MLP_Model_2; main/test or fit_2008/fit_2010/fit_2012 with rolling_evaluation.
- [Annual metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/annual_metrics.csv>) and [Seed metrics](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/seed_metrics.csv>): same filters plus year/seed.
- [Saved absolute intervals](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/metric_intervals.csv>) and [Paired reference intervals](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/outputs_lightweight/extracted/outputs_lightweight/experiment_20261010T052512_046340Z/reports_20261010T102505_608683Z/paired_baseline_comparisons.csv>): same filters plus metric/reference.
- [Workflow](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Hotspot_SameDay_Lightweight/lightweight_workflow.py>): ROLL_SCHEDULES, MAIN_SCHEDULE, run_light_rolling, evaluate_bundle, reference_predictions, create_light_reports.
- [Reviewer 1 major 6](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/reviewer_comments/Reviewer_1.md>); [Reviewer 2 major 5](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/reviewer_comments/Reviewer_2.md>).
- [Audit evidence](<D:/Riset/test/ChatGPT_Peer_Analysis_Start/Temporal_Robustness_Analysis_2026-10-11/audit_evidence.json>): exact hashes, notebook cell IDs/functions and verification counts.
