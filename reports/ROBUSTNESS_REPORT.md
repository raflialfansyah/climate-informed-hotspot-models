# Full-record individual-feature importance robustness review

## Overall assessment: Share with caveats

All 91 frozen region-procedure combinations have been scored on all 2,557 dates with ten repeats in each of four perturbation settings. No models were fitted, recalibrated, selected or discarded. The manuscript, supplement, reviewer forms and pilot exports were left unchanged.

The new calculations replace neither the experimental objective nor the fitted procedures. They test whether the pilot feature rankings persist when date subsampling is removed, Monte Carlo repeats increase, and temporal perturbations change. Detailed rankings remain post hoc model-reliance diagnostics; they are not causal effects, independent validation, or a basis for choosing a new model.

## Key findings

- **The pilot ranks need replacement.** The pilot and full-record ten-repeat reference share a positive leading feature in 55/91 combinations, with median positive-top20 Jaccard overlap 0.538. The matched-first-three comparison below separates the date-sampling contribution from the change in repeat count.
- **Ten repeats support a more detailed variability assessment, not an exact universal order.** For the 30-day reference, first-five versus all-ten means share a positive leader in 84/91 combinations, with median top20 overlap 0.905. The disjoint first-five versus last-five comparison gives 77/91 and 0.739, respectively. Neither comparison is a population confidence interval.
- **Temporal perturbation choice matters.** The positive leading feature set is identical in 76/91 combinations across 7-, 30- and 90-day blocks, but in 50/91 across all four settings. For 30-day versus within-month perturbations, median top20 overlap is 0.429 and median all81 rank correlation is 0.574. The same leading family set persists in 66/91 across all four settings.
- **Recent hotspot history is a recurring model reliance pattern.** It supplies a positive leading feature in 70/91 reference combinations. The two-day log-hotspot lag appears in the positive top20 in 84/91 combinations, the seven-day lag in 81/91, and target-day dry-spell duration in 62/91. These are consistency counts, not physical effect magnitudes or causal findings.

| Setting | History among positive tied leaders | Same positive leader in all 10 repeats | Median within-repeat top20 Jaccard | Median first5 vs10 top20 Jaccard | First5 vs10 leader overlap |
| --- | --- | --- | --- | --- | --- |
| block_30 | 70/91 | 23/91 | 0.497 | 0.905 | 84/91 |
| block_7 | 68/91 | 34/91 | 0.563 | 0.905 | 87/91 |
| block_90 | 66/91 | 29/91 | 0.526 | 0.905 | 81/91 |
| within_month | 68/91 | 16/91 | 0.472 | 0.818 | 83/91 |

## Methodology review: inputs and fixed procedure

- Main S5 fitted procedures: 13 procedures in seven geographic domains, 91 bundles and 203 retained seed estimators.
- Persistence and monthly climatology remain external performance references. They do not use the common fitted 81-column interface and are outside this individual-feature experiment.
- Outcomes: daily aggregate hotspot counts, 1 January 2019 through 31 December 2025, all 2,557 dates in every setting. No sampling weights are required for the complete record.
- Inputs: the adopted 81 engineered columns. A perturbation changes exactly one column; sibling lags and rolling summaries remain fixed.
- Original input scaling, per-seed plain or Duan-smearing count inversion, and equal count-scale seed averaging are retained. Poisson and Tweedie predictions remain on their direct count scale.
- RMSE, MAE, RMSE90 and MAE90 importance is perturbed error minus unperturbed error. R2 importance is baseline R2 minus perturbed R2. Positive values indicate degradation; negative values are retained.
- High days are identified from observed counts using each bundle's original fitting-only threshold. These target dates remain unchanged by the perturbation.

| Domain | Dates | Observed high days | Fitting-only high-day threshold |
| --- | --- | --- | --- |
| Kalimantan | 2557 | 93 | 51.0 |
| National | 2557 | 77 | 156.0 |
| North Sumatra | 2557 | 45 | 29.0 |
| Nusa Tenggara | 2557 | 204 | 6.0 |
| Papua | 2557 | 185 | 3.0 |
| South Sumatra | 2557 | 112 | 21.0 |
| Sulawesi | 2557 | 149 | 3.0 |

## Perturbation settings

The reference setting retains the pilot's 30-day block rule and random seed. Its first three maps are exactly the pilot maps, making the sample-versus-full comparison use matched donor transformations. All settings use ten repeats and shared row maps across features, procedures and regions.

| Setting | Intervention | What it tests |
| --- | --- | --- |
| block_7 | Shuffle consecutive 7-day chunks independently inside each year | Shorter retained local sequences |
| block_30 | Shuffle consecutive 30-day chunks independently inside each year | Reference retained from the pilot |
| block_90 | Shuffle consecutive 90-day chunks independently inside each year | Longer retained local sequences and fewer distinct chunk orders |
| within_month | Shuffle individual dates separately inside each year-month | Constrain donors to the same seasonal month while disrupting short-term order |

All year-end short chunks are retained. No setting fully preserves dependence. In particular, within-month shuffling and year-block shuffling differ in both displacement scale and retained serial structure, so their difference does not isolate a single causal seasonal effect. The within-month setting also leaves month sine/cosine columns unchanged, an expected structural consequence rather than evidence that calendar predictors are globally useless.

## Removing date subsampling

| Comparison | Leader overlap | Median all81 Spearman | Median positive top20 Jaccard |
| --- | --- | --- | --- |
| full_all10 | 55/91 | 0.731 | 0.538 |
| full_first3 | 59/91 | 0.751 | 0.538 |

The full_first3 comparison changes the scoring dates and their weighting while retaining the exact first three perturbation maps. The full_all10 comparison additionally changes Monte Carlo averaging. This separates the date-sampling contribution from the repeat-count contribution.

## Repeat-count assessment

| Setting | Prefix repeats | Leader overlap with all10 | Median all81 Spearman | Median positive top20 Jaccard | Minimum top20 Jaccard |
| --- | --- | --- | --- | --- | --- |
| block_30 | 3 | 80/91 | 0.952 | 0.818 | 0.375 |
| block_30 | 5 | 84/91 | 0.982 | 0.905 | 0.409 |
| block_7 | 3 | 85/91 | 0.953 | 0.818 | 0.500 |
| block_7 | 5 | 87/91 | 0.980 | 0.905 | 0.471 |
| block_90 | 3 | 70/91 | 0.932 | 0.818 | 0.429 |
| block_90 | 5 | 81/91 | 0.981 | 0.905 | 0.538 |
| within_month | 3 | 82/91 | 0.918 | 0.739 | 0.522 |
| within_month | 5 | 83/91 | 0.962 | 0.818 | 0.667 |

A first-five-versus-ten comparison is descriptive and shares its first five maps with the ten-repeat mean. It is not an independent convergence test. Repeat SD and SD/sqrt(10) quantify conditional Monte Carlo variability, not date-sampling uncertainty or population confidence intervals. Ten repeats are an improvement over three, not an automatic guarantee of a stable fine-grained ordering.

A separate comparison uses disjoint first-five and last-five perturbation draws. These are independent sets of Monte Carlo draws conditional on the same dates and frozen models; they are not independent observational replications.

| Setting | First5 vs last5 leader overlap | Median all81 Spearman | Median positive top20 Jaccard |
| --- | --- | --- | --- |
| block_30 | 77/91 | 0.892 | 0.739 |
| block_7 | 80/91 | 0.933 | 0.818 |
| block_90 | 73/91 | 0.917 | 0.739 |
| within_month | 74/91 | 0.860 | 0.667 |

## Sensitivity to temporal perturbation

| Settings | Leader overlap | Median all81 Spearman | Median positive top20 Jaccard | Median changed positive signs |
| --- | --- | --- | --- | --- |
| block_30 / block_7 | 83/91 | 0.950 | 0.818 | 6 |
| block_30 / block_90 | 79/91 | 0.925 | 0.739 | 9 |
| block_30 / within_month | 57/91 | 0.574 | 0.429 | 24 |
| block_7 / block_90 | 80/91 | 0.943 | 0.818 | 7 |
| block_7 / within_month | 57/91 | 0.573 | 0.429 | 24 |
| block_90 / within_month | 53/91 | 0.583 | 0.429 | 25 |

These are matched comparisons of frozen procedures on identical targets. Differences describe reliance under different artificial input disruptions, rather than differences in predictive accuracy of the original models.

### Leading feature versus leading family

A family groups engineered columns by their underlying variable class, such as hotspot history, dry-spell duration, rainfall or IOD. Agreement in this table requires identical nonempty sets of positive tied leaders. A stable family with a changing lag is weaker evidence than agreement on one specific feature. This grouping describes the leading single-column result and is not a joint predictor-group intervention or ablation.

| Domain | Same feature, 3 block lengths | Same family, 3 block lengths | Same feature, all 4 settings | Same family, all 4 settings |
| --- | --- | --- | --- | --- |
| Kalimantan | 11/13 | 12/13 | 5/13 | 8/13 |
| National | 8/13 | 10/13 | 4/13 | 8/13 |
| North Sumatra | 12/13 | 12/13 | 10/13 | 11/13 |
| Nusa Tenggara | 11/13 | 12/13 | 9/13 | 11/13 |
| Papua | 11/13 | 12/13 | 5/13 | 6/13 |
| South Sumatra | 12/13 | 12/13 | 10/13 | 11/13 |
| Sulawesi | 11/13 | 11/13 | 7/13 | 11/13 |

Across all 91 combinations, 50 retain the same positive leading feature set in all four settings; 66 retain the same positive leading family set. These counts are descriptive, with related models and overlapping geographic domains.

## Feature consistency across procedures

Frequency is the number of region-procedure combinations where a feature has positive mean RMSE degradation and rank at most 20, with tied ranks retained. The denominator is 91 in every setting. These combinations are related and are not 91 independent scientific replications. Frequencies describe ranking consistency and do not average effect magnitudes across regions.

| feature | label | block_30 | block_7 | block_90 | within_month |
| --- | --- | --- | --- | --- | --- |
| y_lag_2 | Log hotspot count, lag 2 day(s) | 84 | 83 | 84 | 86 |
| y_lag_7 | Log hotspot count, lag 7 day(s) | 81 | 81 | 77 | 85 |
| y_lag_14 | Log hotspot count, lag 14 day(s) | 76 | 72 | 74 | 61 |
| hth_lag_0 | Dry-spell duration (DS), lag 0 day(s) | 62 | 65 | 62 | 56 |
| y_lag_30 | Log hotspot count, lag 30 day(s) | 54 | 46 | 45 | 42 |
| evap_lag_0 | Signed evaporation, lag 0 day(s) | 52 | 51 | 51 | 64 |
| rain_lag_1 | Rainfall, lag 1 day(s) | 48 | 52 | 50 | 53 |
| wind_lag_0 | Wind speed, lag 0 day(s) | 46 | 56 | 53 | 46 |
| y_rollsum_3 | Previous 3-day log hotspot sum | 46 | 44 | 47 | 27 |
| rain_lag_0 | Rainfall, lag 0 day(s) | 43 | 43 | 50 | 49 |
| rain_rollsum_3 | Rainfall, 3-day sum through target day | 43 | 45 | 48 | 42 |
| y_rollmean_3 | Previous 3-day log hotspot mean | 42 | 42 | 43 | 33 |
| y_lag_21 | Log hotspot count, lag 21 day(s) | 39 | 34 | 30 | 32 |
| y_rollmean_7 | Previous 7-day log hotspot mean | 39 | 40 | 40 | 27 |
| y_lag_3 | Log hotspot count, lag 3 day(s) | 37 | 36 | 32 | 54 |
| y_rollsum_7 | Previous 7-day log hotspot sum | 36 | 37 | 36 | 22 |
| y_lag_1 | Log hotspot count, lag 1 day(s) | 34 | 36 | 38 | 50 |
| hth_lag_3 | Dry-spell duration (DS), lag 3 day(s) | 32 | 29 | 28 | 33 |
| month_sin | Month sine | 31 | 39 | 37 | 0 |
| y_rollmean_30 | Previous 30-day log hotspot mean | 31 | 34 | 30 | 7 |

Separate complete consistency exports are provided for MAE, RMSE90, MAE90 and R2. Their rankings can differ because the error functions emphasize different aspects of prediction error.

## Every region and procedure

The inspection below includes every procedure in every region. The leader is the first alphabetically if tied; the full leaders CSV retains all ties. Delta values are count-scale RMSE increases averaged over ten 30-day-block repeats. The Jaccard columns compare positive top20 sets with the reference 30-day setting. High-day results and all five metric differences are in the complete procedure exports.

### Kalimantan

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Dry-spell duration (DS), lag 1 day(s) | 106.966 | 54.556 | 1.000 | 0.818 | 0.739 | 0.379 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 9.938 | 3.427 | 1.000 | 0.905 | 0.905 | 0.538 |
| KNN | Dry-spell duration (DS), lag 0 day(s) | 1.940 | 0.856 | 0.818 | 0.667 | 0.379 | 0.379 |
| LightGBM | Log hotspot count, lag 2 day(s) | 10.119 | 3.739 | 0.905 | 1.000 | 0.905 | 0.333 |
| MLP_Model_1 | Dry-spell duration (DS), lag 0 day(s) | 6.004 | 2.799 | 0.818 | 0.667 | 0.600 | 0.481 |
| MLP_Model_2 | Log hotspot count, lag 1 day(s) | 16.235 | 5.097 | 0.739 | 0.667 | 0.739 | 0.739 |
| MLP_Model_3 | Dry-spell duration (DS), lag 0 day(s) | 8.726 | 3.251 | 0.905 | 0.905 | 0.818 | 0.333 |
| MLP_Model_4 | Log hotspot count, lag 1 day(s) | 38.383 | 18.403 | 0.905 | 0.818 | 0.818 | 0.481 |
| Poisson | Dry-spell duration (DS), lag 3 day(s) | 30.408 | 15.606 | 1.000 | 0.818 | 0.739 | 0.538 |
| RandomForest | Log hotspot count, lag 2 day(s) | 12.709 | 4.357 | 0.818 | 0.905 | 0.818 | 0.600 |
| SVM_RBF | Dry-spell duration (DS), lag 0 day(s) | 3.522 | 2.562 | 0.667 | 0.600 | 0.667 | 0.481 |
| Tweedie | Dry-spell duration (DS), lag 3 day(s) | 9.840 | 4.967 | 0.905 | 0.667 | 0.739 | 0.600 |
| XGBoost | Log hotspot count, lag 2 day(s) | 10.382 | 3.820 | 0.905 | 0.905 | 0.818 | 0.481 |

### National

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Log hotspot count, lag 2 day(s) | 17.497 | 7.998 | 1.000 | 0.818 | 0.905 | 0.600 |
| ExtraTrees | Previous 3-day log hotspot mean | 9.857 | 5.527 | 1.000 | 0.905 | 0.905 | 0.600 |
| KNN | Dry-spell duration (DS), lag 1 day(s) | 1.665 | 1.676 | 0.739 | 0.783 | 0.667 | 0.429 |
| LightGBM | Log hotspot count, lag 2 day(s) | 12.800 | 5.358 | 0.818 | 0.818 | 0.739 | 0.481 |
| MLP_Model_1 | Dry-spell duration (DS), lag 1 day(s) | 2.519 | 2.879 | 0.538 | 0.538 | 0.481 | 0.538 |
| MLP_Model_2 | Log hotspot count, lag 2 day(s) | 6.062 | 3.762 | 0.905 | 0.818 | 0.739 | 0.333 |
| MLP_Model_3 | Log hotspot count, lag 2 day(s) | 4.113 | 4.532 | 0.667 | 0.600 | 0.538 | 0.212 |
| MLP_Model_4 | Log hotspot count, lag 2 day(s) | 5.726 | 3.439 | 1.000 | 1.000 | 0.818 | 0.429 |
| Poisson | Log hotspot count, lag 2 day(s) | 18.400 | 8.447 | 1.000 | 0.818 | 1.000 | 0.600 |
| RandomForest | Previous 3-day log hotspot mean | 14.437 | 7.773 | 0.905 | 0.905 | 0.905 | 0.667 |
| SVM_RBF | Dry-spell duration (DS), lag 0 day(s) | 7.109 | 4.489 | 0.905 | 0.905 | 0.667 | 0.333 |
| Tweedie | Log hotspot count, lag 2 day(s) | 11.639 | 6.305 | 0.864 | 0.818 | 0.818 | 0.640 |
| XGBoost | Previous 3-day log hotspot mean | 15.281 | 9.142 | 0.818 | 0.905 | 0.739 | 0.429 |

### North Sumatra

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Log hotspot count, lag 2 day(s) | 1.506 | 0.337 | 0.905 | 0.905 | 0.818 | 0.538 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 0.644 | 0.239 | 0.818 | 0.667 | 0.481 | 0.429 |
| KNN | Log hotspot count, lag 3 day(s) | 0.039 | 0.039 | 0.409 | 0.412 | 0.350 | 0.174 |
| LightGBM | Log hotspot count, lag 2 day(s) | 0.923 | 0.234 | 0.818 | 0.739 | 0.739 | 0.667 |
| MLP_Model_1 | ROMI1, lag 3 day(s) | 3.138 | 2.219 | 0.739 | 0.538 | 0.600 | 0.290 |
| MLP_Model_2 | Log hotspot count, lag 2 day(s) | 0.887 | 0.283 | 0.905 | 1.000 | 0.667 | 0.429 |
| MLP_Model_3 | Log hotspot count, lag 2 day(s) | 0.613 | 0.352 | 0.739 | 0.667 | 0.667 | 0.429 |
| MLP_Model_4 | Log hotspot count, lag 2 day(s) | 0.925 | 0.335 | 0.739 | 0.818 | 0.739 | 0.429 |
| Poisson | Log hotspot count, lag 3 day(s) | 2.814 | 0.528 | 0.905 | 0.739 | 0.739 | 0.538 |
| RandomForest | Log hotspot count, lag 2 day(s) | 0.744 | 0.258 | 0.818 | 0.538 | 0.538 | 0.600 |
| SVM_RBF | Previous 30-day log hotspot std | 0.876 | 0.426 | 0.739 | 0.667 | 0.600 | 0.481 |
| Tweedie | Log hotspot count, lag 3 day(s) | 0.827 | 0.148 | 1.000 | 0.783 | 0.538 | 0.667 |
| XGBoost | Log hotspot count, lag 2 day(s) | 0.804 | 0.250 | 0.818 | 0.818 | 0.600 | 0.538 |

### Nusa Tenggara

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Dry-spell duration (DS), lag 3 day(s) | 1.809 | 0.500 | 0.905 | 0.905 | 0.905 | 0.379 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 0.539 | 0.135 | 0.905 | 1.000 | 1.000 | 0.250 |
| KNN | Log hotspot count, lag 2 day(s) | 0.181 | 0.052 | 0.818 | 0.818 | 0.905 | 0.212 |
| LightGBM | Log hotspot count, lag 2 day(s) | 0.531 | 0.122 | 1.000 | 0.905 | 0.905 | 0.379 |
| MLP_Model_1 | Previous 60-day log hotspot mean | 0.313 | 0.064 | 0.818 | 0.739 | 0.667 | 0.176 |
| MLP_Model_2 | Log hotspot count, lag 2 day(s) | 0.307 | 0.076 | 0.905 | 1.000 | 0.905 | 0.250 |
| MLP_Model_3 | Log hotspot count, lag 2 day(s) | 0.330 | 0.079 | 1.000 | 1.000 | 0.905 | 0.290 |
| MLP_Model_4 | Log hotspot count, lag 2 day(s) | 0.187 | 0.106 | 0.818 | 0.739 | 0.739 | 0.176 |
| Poisson | Log hotspot count, lag 2 day(s) | 0.223 | 0.096 | 0.818 | 0.739 | 0.739 | 0.429 |
| RandomForest | Log hotspot count, lag 2 day(s) | 0.508 | 0.128 | 0.905 | 0.905 | 0.905 | 0.250 |
| SVM_RBF | Dry-spell duration (DS), lag 3 day(s) | 0.130 | 0.041 | 0.905 | 0.600 | 0.538 | 0.333 |
| Tweedie | Log hotspot count, lag 2 day(s) | 0.114 | 0.062 | 0.905 | 0.905 | 0.818 | 0.429 |
| XGBoost | Log hotspot count, lag 2 day(s) | 0.511 | 0.113 | 0.905 | 0.905 | 0.905 | 0.290 |

### Papua

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Log hotspot count, lag 2 day(s) | 0.295 | 0.064 | 0.905 | 1.000 | 1.000 | 0.429 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 0.132 | 0.035 | 0.905 | 1.000 | 0.905 | 0.429 |
| KNN | Log hotspot count, lag 7 day(s) | 0.160 | 0.033 | 0.864 | 0.739 | 0.667 | 0.333 |
| LightGBM | Log hotspot count, lag 7 day(s) | 0.227 | 0.053 | 0.818 | 0.739 | 0.905 | 0.429 |
| MLP_Model_1 | Log hotspot count, lag 2 day(s) | 0.189 | 0.049 | 0.905 | 0.667 | 0.818 | 0.250 |
| MLP_Model_2 | Log hotspot count, lag 7 day(s) | 0.222 | 0.048 | 0.818 | 0.739 | 0.739 | 0.481 |
| MLP_Model_3 | Log hotspot count, lag 7 day(s) | 0.303 | 0.074 | 0.905 | 0.667 | 0.600 | 0.379 |
| MLP_Model_4 | Log hotspot count, lag 7 day(s) | 0.231 | 0.048 | 1.000 | 0.905 | 0.905 | 0.379 |
| Poisson | Log hotspot count, lag 2 day(s) | 0.276 | 0.065 | 0.905 | 1.000 | 0.905 | 0.429 |
| RandomForest | Rainfall, 3-day sum through target day | 0.141 | 0.047 | 0.905 | 0.905 | 0.905 | 0.538 |
| SVM_RBF | Dry-spell duration (DS), lag 0 day(s) | 0.115 | 0.029 | 0.905 | 0.818 | 0.905 | 0.379 |
| Tweedie | Log hotspot count, lag 2 day(s) | 0.202 | 0.046 | 1.000 | 0.905 | 0.818 | 0.538 |
| XGBoost | Log hotspot count, lag 7 day(s) | 0.217 | 0.052 | 1.000 | 1.000 | 0.818 | 0.429 |

### South Sumatra

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Dry-spell duration (DS), lag 1 day(s) | 37.326 | 14.741 | 1.000 | 1.000 | 0.739 | 0.481 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 3.693 | 1.637 | 0.905 | 1.000 | 1.000 | 0.667 |
| KNN | Log hotspot count, lag 2 day(s) | 1.727 | 1.002 | 1.000 | 0.905 | 0.818 | 0.379 |
| LightGBM | Log hotspot count, lag 2 day(s) | 4.042 | 1.808 | 0.905 | 0.818 | 0.818 | 0.600 |
| MLP_Model_1 | Log hotspot count, lag 2 day(s) | 4.158 | 2.249 | 1.000 | 0.818 | 0.818 | 0.429 |
| MLP_Model_2 | Log hotspot count, lag 2 day(s) | 1.194 | 0.477 | 1.000 | 0.905 | 1.000 | 0.333 |
| MLP_Model_3 | Log hotspot count, lag 2 day(s) | 3.764 | 2.016 | 0.739 | 0.667 | 0.667 | 0.538 |
| MLP_Model_4 | Dry-spell duration (DS), lag 7 day(s) | 4.764 | 1.170 | 0.818 | 0.739 | 0.739 | 0.538 |
| Poisson | Log hotspot count, lag 2 day(s) | 4.579 | 2.139 | 0.818 | 0.739 | 0.739 | 0.429 |
| RandomForest | Log hotspot count, lag 2 day(s) | 3.675 | 1.679 | 0.818 | 0.905 | 0.818 | 0.667 |
| SVM_RBF | Dry-spell duration (DS), lag 0 day(s) | 2.576 | 1.680 | 0.905 | 0.600 | 0.538 | 0.250 |
| Tweedie | Log hotspot count, lag 2 day(s) | 3.841 | 1.861 | 0.905 | 1.000 | 0.905 | 0.667 |
| XGBoost | Log hotspot count, lag 2 day(s) | 3.920 | 1.758 | 0.818 | 0.905 | 0.905 | 0.538 |

### Sulawesi

| Procedure | Leading feature | Mean delta RMSE | Repeat SD | First5/10 Jaccard | 7/30 Jaccard | 30/90 Jaccard | 30/month Jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BayesianRidge | Dry-spell duration (DS), lag 3 day(s) | 0.287 | 0.132 | 0.905 | 0.818 | 0.818 | 0.481 |
| ExtraTrees | Log hotspot count, lag 2 day(s) | 0.255 | 0.084 | 0.905 | 0.739 | 0.739 | 0.481 |
| KNN | Log hotspot count, lag 2 day(s) | 0.073 | 0.046 | 0.667 | 0.538 | 0.667 | 0.481 |
| LightGBM | Log hotspot count, lag 2 day(s) | 0.175 | 0.090 | 0.739 | 0.739 | 0.600 | 0.379 |
| MLP_Model_1 | Log hotspot count, lag 7 day(s) | 0.253 | 0.084 | 0.818 | 0.667 | 0.600 | 0.333 |
| MLP_Model_2 | Signed evaporation, lag 0 day(s) | 0.215 | 0.121 | 0.905 | 0.818 | 0.818 | 0.600 |
| MLP_Model_3 | Log hotspot count, lag 7 day(s) | 0.147 | 0.070 | 0.905 | 0.600 | 0.667 | 0.538 |
| MLP_Model_4 | Signed evaporation, lag 0 day(s) | 0.499 | 0.451 | 1.000 | 0.739 | 0.818 | 0.600 |
| Poisson | Log hotspot count, lag 2 day(s) | 0.194 | 0.065 | 0.905 | 0.818 | 0.818 | 0.538 |
| RandomForest | Log hotspot count, lag 2 day(s) | 0.180 | 0.069 | 0.739 | 0.667 | 0.600 | 0.379 |
| SVM_RBF | Log hotspot count, lag 7 day(s) | 0.168 | 0.061 | 0.818 | 0.667 | 0.481 | 0.143 |
| Tweedie | Log hotspot count, lag 2 day(s) | 0.142 | 0.045 | 0.905 | 0.739 | 0.739 | 0.481 |
| XGBoost | Log hotspot count, lag 2 day(s) | 0.176 | 0.085 | 0.818 | 0.739 | 0.739 | 0.481 |

## Calculation spot-checks and boundaries

- All 91 original pilot procedure exports were read and their 22,113 repeat rows and 7,371 mean scores checked.
- All 364 full-record setting exports, 294,840 perturbation scores and 29,484 mean scores were checked for completeness, identities, finiteness, signs, and stored hashes.
- Every one of the 203 retained seeds reproduced its original saved prediction on all 2,557 dates within the declared tolerance (rtol 2e-5, absolute tolerance 0.002 counts). Neural float rounding remains within this combined tolerance.
- Independent original-estimator replays: 624 perturbed score cases; the verification file records exact cases and numerical differences.
- Linear-link, RBF-factorization and forest-path accelerations were separately compared against the original estimator predictions for every affected region/procedure. Other procedures reuse predictions only for exactly identical input rows, with exact row-context and donor-value round-trip checks. Scheduling and algebra changed, fitted models and intervention definitions did not.
- All 2,405 protected files retained their starting hashes. The manuscript and supplementary PDFs retain their pre-run hashes.
- CSV precision QA caught a serialization-reader issue: the default float parser could collapse adjacent scores into apparent ties. Aggregation, verification and reporting now use round-trip float parsing. The previous derived summaries and failed check are archived in evidence/before_roundtrip_reader_fix, with the diagnosis and numerical impact recorded in reader_precision_fix.json and reader_precision_impact.json.
- Correcting the reader changed mean RMSE importance by at most 1.42e-14 counts and high-day error importance by at most 2.85e-14 counts. One of 1,620 metric-setting-feature frequency counts changed by one; the reference 30-day RMSE frequencies and leading-feature/family agreement totals were unchanged. The 624 completed native replays were retained with a locked hash and their metric comparisons checked again against the precise primary exports. Near-identical engineered-feature scores at machine precision do not support a substantive ordering.
- No source-calendar or native-unit issue was resolved by importance scoring. The existing dry-spell calendar and other upstream provenance qualifications still apply.

## Visual review

No manuscript figure, PDF or layout was changed. The tables in this report are generated from the verified exports; the full numerical tables remain available as CSV files. The existing manuscript Figure 8 still displays the earlier pilot.

## Suggested manuscript improvements

Do not treat the restored pilot Figure 8 frequencies or its 735-date/three-repeat wording as final. This report supplies the full-record replacement evidence, but the manuscript has intentionally not been edited in this task. A later integration must use the complete setting comparison to distinguish broad recurring predictor groups from individual lag rankings that change with the perturbation rule.

## Relationship to reviewer requests

- Reviewer 4, Major Comment 4, and Reviewer 2, Additional Clarifications 6, ask how importance is made comparable across model families. All fitted procedures here use the same single-column intervention and count-scale error criterion inside each region, including their fixed input scalers and output inversions. Native tree gains and regression coefficients are not pooled. Raw count-scale effect sizes are not averaged across regions.
- Reviewer 4 also distinguishes top20 frequency from effect magnitude. The frequency tables count positive top20 rank occurrence; procedure exports separately retain loss changes and repeat spread. Top20 occurrence is not a new feature-selection stage: all original 81 inputs remain in every fitted procedure.
- Reviewer 3, Figure 8, asks for descriptive labels. These exports include human-readable labels and explicit lag/rolling-window meanings. The existing manuscript figure remains the pilot version until later integration.
- The incremental value of climate beyond hotspot history is a separate predictor-group ablation question. Individual-column perturbations do not replace the matched group-ablation experiment.
- Sensitivity to temporal perturbation choices tests interpretation of fixed-model importance. It does not itself provide rolling-origin generalization evidence or replace the separate earlier-prefix temporal evaluation.

## Reproducibility files

- protocol.json: fixed design, seeds, settings, scope and inference limits.
- robustness.py: frozen-model inference with digest-checked resumable per-setting exports.
- review_results.py: arithmetic, completeness, repeat-prefix and setting comparisons.
- verify_replays.py: independent full-record replay and map reconstruction checks.
- results/: 364 procedure-specific CSV files and their completion identities.
- importance_replicates.csv / importance_summary.csv: complete repeat scores and means for all five metrics.
- pilot_vs_full_ranking.csv, repeat_prefix_comparison.csv, repeat_ranking_stability.csv, perturbation_sensitivity.csv: ranking robustness evidence.
- evidence/: source hashes, 91 replay audits, donor maps, diagnostics, complete validations and protected-file checks.
