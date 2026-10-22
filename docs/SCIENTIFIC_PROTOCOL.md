# Scientific protocol

The target is a daily aggregate hotspot count on day t. Environmental observations through t and observed hotspot history through t-1 are supplied. The task is retrospective same-day estimation, not recursive advance forecasting. The 2019-2025 record is analyst-exposed.

The main fitting prefix ends on 31 December 2014. A common 60-day warm-up leaves 5,053 fitting dates. Calibration in 2015-2016 has 731 dates; inverse selection in 2017-2018 has 730; scoring in 2019-2025 has 2,557. Source SST reference months are restricted to the fitting prefix, with the available pre-2001 context retained by the loader.

Each estimator is fitted once per declared seed and procedure. For a log-target model, S = mean(exp(log1p(y_cal) - z_cal)). The smeared inverse is max(S * exp(z) - 1, 0); the plain inverse is max(exp(z) - 1, 0). Selection-period count RMSE chooses the inverse with strict improvement; ties choose plain. Seed-wise count predictions are averaged equally after inversion. Direct Poisson and Tweedie responses bypass log-target inversion. Calibration and inverse selection add no estimator fits. No final refit or Lasso feature selection is performed.

The 13 fitted procedures are Bayesian Ridge, Random Forest, Extra Trees, XGBoost, LightGBM, SVM-RBF, KNN, four MLP architectures, Poisson and Tweedie. Persistence and training-only Monthly Climatology are unfitted references. Seven domains are evaluated separately. Stochastic seeds are 42, 137 and 2026; deterministic procedures use seed 42 once. All declared seeds are retained.

S2 has calendar and history (26 features), S3 calendar and environment without history (59), S4 calendar, history and local environment (54), and S5 all groups (81). Bayesian Ridge and MLP 2 are the fixed representatives for matched group ablation and earlier temporal evaluations. Ablation arms retain dates, estimator settings and seeds but independently calibrate and select their inverse, so contrasts concern complete procedures.

Earlier fitting ends are 2008, 2010 and 2012, each followed by separate two-year calibration, selection and scoring blocks. Their scoring windows are 2013-2014, 2015-2016 and 2017-2018. Original fit count is 203 + 84 + 84 = 371.

The 15 count metrics are RMSE, MAE, R2, signed bias, SMAPE, MAE90, RMSE90, POD, FAR, CSI, hits, misses, false alarms, correct negatives and zero-day false detections. The high-day threshold is ceil(raw fitting-period count p90), including warm-up dates. High days and predicted events use an inclusive threshold. MAE90 and RMSE90 score errors on observed high days. Zero-day false detections require observed zero and a prediction reaching the high-day threshold. Undefined denominators remain unavailable.

Intervals use 500 common whole-year resamples with seed 42 and unadjusted percentile limits. They are conditional metric intervals, not daily prediction intervals; few year blocks and multiple comparisons limit inference. Rainfall-defined dry/wet strata are retrospective project adaptations, not verified official regional seasonal-zone calendars.

The later individual-feature experiment holds fitted models, scalers and seed-specific inverses fixed. It covers 91 fitted procedure-domain bundles, 81 columns, 2,557 dates, 10 repeats and four perturbation settings, yielding 294,840 replicate scores. It measures exploratory reliance, not causal effects or feature selection. Correlated engineered columns can produce inconsistent perturbed inputs. All settings and repeat diagnostics remain available.
