"""Recalculate all 15 main metrics from packaged predictions, without fitting."""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from release_io import ROOT, read_table


def evaluate(y, p, threshold):
    e = p - y
    h, ph = y >= threshold, p >= threshold
    hits, misses, false = int((h & ph).sum()), int((h & ~ph).sum()), int((~h & ph).sum())
    div = lambda a, b: a / b if b else np.nan
    variance = np.square(y - y.mean()).sum()
    smape = np.divide(200 * np.abs(e), y + p, out=np.zeros_like(y), where=(y + p) != 0)
    return dict(rmse_count=np.sqrt(np.mean(e * e)), mae_count=np.mean(abs(e)),
        r2_count=1 - div(np.square(e).sum(), variance), bias_count=e.mean(), smape_count=smape.mean(),
        mae90_count=np.mean(abs(e[h])) if h.any() else np.nan,
        rmse90_count=np.sqrt(np.mean(e[h] ** 2)) if h.any() else np.nan,
        pod=div(hits, hits + misses), far=div(false, hits + false), csi=div(hits, hits + misses + false),
        hits=hits, misses=misses, false_alarms=false, correct_negatives=int((~h & ~ph).sum()),
        zero_day_false_detections=int(((y == 0) & ph).sum()))


def main():
    main = read_table('aggregate_predictions.csv', parse_dates=['target_date']).query(
        'schedule == "main" and group == "S5" and partition == "test"')
    refs = read_table('reference_predictions.csv', parse_dates=['target_date']).query(
        'schedule == "main" and partition == "test"')
    reported = read_table('main_full_metrics.csv').set_index(['unit', 'model'])
    assert len(reported) == 105 and reported.index.is_unique
    expected = pd.date_range('2019-01-01', '2025-12-31')
    series = dict(tuple(pd.concat([main, refs], ignore_index=True).groupby(['unit', 'model'])))
    assert len(series) == 105
    maximum = 0.
    comparisons = 0
    for key, frame in series.items():
        frame = frame.sort_values('target_date')
        assert pd.DatetimeIndex(frame.target_date).equals(expected)
        y, p = frame.actual.to_numpy(float), frame.prediction.to_numpy(float)
        assert np.isfinite(y).all() and np.isfinite(p).all() and (y >= 0).all() and (p >= 0).all()
        reference_y = series[(key[0], 'Persistence')].sort_values('target_date').actual.to_numpy()
        assert np.array_equal(y, reference_y)
        row = reported.loc[key]
        result = evaluate(y, p, float(row.threshold))
        for metric, value in result.items():
            target = row[metric]
            assert np.isclose(value, target, rtol=1e-10, atol=1e-10, equal_nan=True), (key, metric, value, target)
            if np.isfinite(value) and np.isfinite(target):
                maximum = max(maximum, abs(value - target))
            comparisons += 1
    out = dict(passed=True, series=105, domains=7, dates_per_series=2557,
        metric_values_recomputed=comparisons, maximum_absolute_difference=maximum,
        new_estimator_fits=0, new_model_inference=0)
    (ROOT / 'validation').mkdir(exist_ok=True)
    (ROOT / 'validation/result_checks.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
