"""Validate published aggregates and reconstruct every schedule's features; zero fits."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import main_scheme as scheme


def main():
    config=scheme.RebuildConfig(processed_dir=ROOT/'data/processed')
    frames,_=scheme.load_region_daily_frames(config)
    manifest=json.loads((config.processed_dir/'processed_input_manifest.json').read_text())
    records=[]
    for unit,frame in frames.items():
        values=frame.drop(columns='issue_date').to_numpy()
        assert hashlib.sha256(values.tobytes()).hexdigest()==manifest['original_numeric_sha256'][unit],unit
        for schedule in (scheme.MAIN_SCHEDULE,*scheme.ROLL_SCHEDULES):
            view=scheme.preparation(frame,schedule)
            full,groups,metadata=scheme.prepare_fit(frame,schedule.fit_end)
            assert {k:len(groups[k]) for k in ('S2','S3','S4','S5')}=={'S2':26,'S3':59,'S4':54,'S5':81}
            assert len(full)==9071 and len(metadata['excluded_dates'])==60
            score=full[full.target_date.between(schedule.score_start,schedule.score_end)]
            assert pd.DatetimeIndex(score.target_date).equals(pd.date_range(schedule.score_start,schedule.score_end))
            records.append(dict(unit=unit,schedule=schedule.name,training_rows=metadata['training_rows'],score_rows=len(score),features=81,threshold=view['threshold']))
    sst=next(iter(frames.values())).attrs['raw_sst']
    assert hashlib.sha256(sst.drop(columns='issue_date').to_numpy().tobytes()).hexdigest()==manifest['sst_numeric_sha256']
    report=dict(passed=True,domains=len(frames),daily_rows=sum(len(f) for f in frames.values()),
        dates_per_domain=9131,sst_context_dates=len(sst),schedule_domain_checks=len(records),
        original_numeric_hashes_match=True,feature_columns=81,warmup_days=60,new_estimator_fits=0,new_model_inference=0,checks=records)
    output=ROOT/'validation/processed_input_checks.json';output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))


if __name__=='__main__':main()
