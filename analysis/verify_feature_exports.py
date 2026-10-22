"""Recalculate full-record feature means and ranks from all 364 bundled exports."""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from release_io import ROOT, read_table


def main():
    paths = sorted((ROOT / 'results/individual_feature/procedure_exports').glob('*.csv'))
    assert len(paths) == 364
    parts = [pd.read_csv(p, float_precision='round_trip') for p in paths]
    assert all(len(p) == 810 for p in parts)
    frame = pd.concat(parts, ignore_index=True)
    keys = ['setting', 'unit', 'model', 'feature']
    assert len(frame) == 294840 and not frame.duplicated(keys + ['repeat']).any()
    assert frame.n.eq(2557).all() and set(frame.repeat) == set(range(10))
    assert frame.setting.nunique() == 4 and frame.feature.nunique() == 81
    summary = read_table('individual_feature_importance_summary.csv').set_index(keys).sort_index()
    grouped = frame.groupby(keys)
    assert grouped.size().eq(10).all()
    metrics = ['rmse', 'mae', 'rmse90', 'mae90', 'r2']
    differences = {}
    for metric in metrics:
        means = grouped['delta_' + metric].mean().sort_index()
        assert means.index.equals(summary.index)
        assert np.allclose(means, summary['delta_' + metric], rtol=1e-10, atol=1e-11)
        differences[metric] = float(np.max(np.abs(means - summary['delta_' + metric])))
    ranks = summary.groupby(['setting', 'unit', 'model']).delta_rmse.rank(method='min', ascending=False)
    assert np.array_equal(ranks, summary.rank_rmse)
    result = dict(passed=True, procedure_exports=364, replicate_scores=len(frame),
        feature_means=len(summary), mean_metric_checks=len(summary)*5,
        rmse_ranks_checked=len(ranks), maximum_absolute_differences=differences,
        new_estimator_fits=0, new_model_inference=0)
    (ROOT / 'validation/feature_export_checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
