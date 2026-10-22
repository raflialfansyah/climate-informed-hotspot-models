"""Frozen-model, full-record individual-feature sensitivity experiment.

No manuscript edits, estimator fits, calibration or model selection are allowed.
All choices below are fixed before the first new perturbation result is scored.
"""
from pathlib import Path
import os
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
os.environ.setdefault('OMP_NUM_THREADS', '4')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '4')
import sys, json, time, pickle, gc, importlib.util, itertools
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

import argparse
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from release_io import ROOT as REPO, local_paths
ROOT = REPO / 'generated/individual_feature'
PILOT = REPO / 'results/individual_feature'
import _inference as p
p.ROOT = ROOT
REPEATS = 10
SETTINGS = [('block_30',30,20261018), ('block_7',7,20261025),
            ('block_90',90,20261108), ('within_month',None,20261118)]

def protocol():
    return dict(version=1, scope='91 main S5 frozen region-procedure bundles, all 81 features, all retained seeds',
      score_dates=['2019-01-01','2025-12-31'], n=2557, repeats=REPEATS,
      settings=[dict(name=n,block_days=b,seed=s) for n,b,s in SETTINGS],
      perturbation_unit='one already engineered column; outcomes and other columns unchanged',
      block_rule='Partition each calendar year into consecutive fixed-length chunks, retain final short chunk, randomly reorder chunks; reject identity orders',
      month_rule='Independently permute individual dates inside each year-month; preserves the monthly marginal distribution but destroys within-month serial order',
      shared_maps='Same maps for every feature, model and region; independent setting RNG seeds',
      score='Unweighted count-scale RMSE, MAE, RMSE90, MAE90; baseline R2 minus perturbed R2',
      high_days='Observed count at least original fitting-only saved threshold, identical target rows before/after perturbation',
      fixed='Original scaler, fitted weights, per-seed inversion and equal count-scale seed average; zero estimator fits',
      rationale='Ten repeats improve Monte Carlo assessment relative to three; 7/30/90-day blocks vary retained local order and displacement; within-month shuffling probes the contribution of disrupting seasonal timing',
      inference_limits=['Post hoc reliance on an already exposed retrospective record, not independent confirmation or a selection exercise',
        'Correlated engineered columns remain unchanged, creating potentially inconsistent inputs and masking/substitution effects',
        'No permutation scheme fully preserves dependence; within-month and block settings have different intervention strengths',
        'Repeat SD/SE and prefix stability describe Monte Carlo variation conditional on dates and models, not population confidence intervals',
        'No guarantee that ten repeats are sufficient: compare first 3/5 with all 10 and report unstable rankings',
        'Inherited predictor calendar/unit provenance qualifications remain unresolved'],
      comparisons=['Pilot 735 dates/3 repeats versus full 2557 dates/first 3 identical block_30 maps',
        'Full block_30 first 3/5 versus 10 repeats',
        'All six pairs of perturbation settings on the full record, same 10-repeat count'],
      ordering='All settings reported; block_30 retained as reference from the pilot, not selected using the new results',
      expected_scores=91*81*REPEATS*len(SETTINGS))

def make_maps(dates):
    dates=pd.DatetimeIndex(dates); years=dates.year.to_numpy(); out={}; records=[]
    for name,block,seed in SETTINGS:
        rng=np.random.default_rng(seed); maps=[]
        for repeat in range(REPEATS):
            index=np.arange(len(dates))
            groups=sorted(set(zip(years,dates.month))) if block is None else sorted(set(years))
            for group in groups:
                if block is None:
                    year,month=group
                    rows=np.flatnonzero((years==year)&(dates.month==month))
                    order=rng.permutation(len(rows))
                    while np.array_equal(order,np.arange(len(rows))): order=rng.permutation(len(rows))
                    index[rows]=rows[order]
                else:
                    rows=np.flatnonzero(years==group)
                    chunks=[rows[i:i+block] for i in range(0,len(rows),block)]
                    order=rng.permutation(len(chunks))
                    while np.array_equal(order,np.arange(len(chunks))): order=rng.permutation(len(chunks))
                    index[rows]=np.concatenate([chunks[i] for i in order])
                records.append(dict(setting=name,repeat=repeat,group=str(group),order=order.tolist()))
            assert np.array_equal(np.sort(index),np.arange(len(dates)))
            assert np.array_equal(years[index],years)
            if block is None: assert np.array_equal(dates.month[index],dates.month)
            maps.append(index)
        out[name]=np.asarray(maps)
    old=np.load(PILOT/'individual_feature_permutation_indices.npz')
    assert all(np.array_equal(out[name],old[name]) for name in out)
    return out,records

def initialize():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'evidence').mkdir(exist_ok=True); (ROOT/'results').mkdir(exist_ok=True)
    plan=protocol(); encoded=json.dumps(plan,sort_keys=True).encode('utf-8')
    import hashlib
    digest=hashlib.sha256(encoded).hexdigest()
    if (ROOT/'protocol.json').exists():
        assert json.loads((ROOT/'protocol.json').read_text(encoding='utf-8'))==plan
        return digest
    p.write_json(ROOT/'protocol.json',plan)
    files=p.file_inventory()
    files.update({str(f):p.sha(f) for f in PILOT.rglob('*') if f.is_file()})
    p.write_json(ROOT/'evidence/protected_before.json',files)
    p.write_json(ROOT/'evidence/design_identity.json',dict(protocol_sha256=digest,runner_sha256=p.sha(__file__)))
    return digest

def linear_disruptor(m,predict,x):
    """Exact single-column linear-predictor update; checked against saved estimator."""
    if len(predict.estimators)!=1: return None,[]
    _,pipe,decision=predict.estimators[0]
    model=pipe.named_steps['model']; scaler=pipe.named_steps['scaler']
    coef=np.asarray(model.coef_).reshape(-1)
    assert len(coef)==x.shape[1]
    baseline_raw=np.asarray(pipe.predict(x)).reshape(-1)
    direct=model.__class__.__name__ in ('PoissonRegressor','TweedieRegressor')
    def disrupted(column,donors):
        j=x.columns.get_loc(column)
        offset=(x[column].to_numpy()[donors]-x[column].to_numpy())*coef[j]/scaler.scale_[j]
        raw=baseline_raw*np.exp(offset) if direct else baseline_raw+offset
        return np.maximum(raw,0) if direct else m.inverse_log1p_smearing(raw,decision['effective_factor'])
    errors=[]
    for column in ['y_lag_1','hth_lag_0']:
        donors=np.roll(np.arange(len(x)),17)
        variant=x.copy();variant[column]=x[column].to_numpy()[donors]
        exact=predict(variant);fast=disrupted(column,donors)
        errors.append(float(np.max(np.abs(exact-fast))))
        assert np.allclose(exact,fast,rtol=1e-9,atol=1e-8)
    return disrupted,errors

def run():
    digest=initialize();m=p.load_helpers();frames=pickle.load(p.FRAMES.open('rb'))
    records=[]
    for path in sorted((p.EXPERIMENT/'procedures/main').glob('*/S5/*/bundle.json')):
        meta=json.loads(path.read_text(encoding='utf-8'))
        records.append(dict(unit=meta['unit'],model=meta['candidate']['name'],folder=str(path.parent)))
    inventory=pd.DataFrame(records)
    assert len(inventory)==91
    maps=None;cache={};all_start=time.perf_counter()
    for number,record in inventory.iterrows():
        folder=Path(record.folder);slug=folder.parts[-3]
        destinations={s:ROOT/'results'/f'{slug}__{record.model}__{s}.csv' for s,_,_ in SETTINGS}
        if all(f.exists() and f.with_suffix('.complete.json').exists() for f in destinations.values()):
            for f in destinations.values():
                done=json.loads(f.with_suffix('.complete.json').read_text(encoding='utf-8'))
                assert done['protocol_sha256']==digest and p.sha(f)==done['sha256']
            print(f'REUSE {number+1}/91 {record.unit}/{record.model}',flush=True);continue
        start=time.perf_counter();meta,predict=p.get_predictor(m,folder)
        if record.unit not in cache:
            f,_,_=m.prepare_fit(frames[record.unit],meta['schedule']['fit_end'])
            cache.clear()
            cache[record.unit]=f.loc[f.target_date.between('2019-01-01','2025-12-31')].reset_index(drop=True)
        rows=cache[record.unit];x=rows[meta['columns']].copy();original=x.to_numpy(copy=True)
        assert len(rows)==2557 and x.shape==(2557,81)
        y=rows.target_count.to_numpy(); high=y>=meta['threshold']['threshold']
        # Every seed is replayed on the full record before any perturbation score.
        seed_values=predict(x,True)
        saved=pd.read_csv(folder/'evaluation/seed_predictions.csv',parse_dates=['target_date'])
        seed_checks=[]
        for seed,values in zip(meta['seeds'],seed_values):
            old=saved[saved.seed.eq(seed)].sort_values('target_date')
            assert np.array_equal(rows.target_date.to_numpy(),old.target_date.to_numpy())
            assert np.array_equal(y,old.actual.to_numpy())
            assert np.allclose(values,old.prediction,rtol=2e-5,atol=.002)
            seed_checks.append(dict(seed=seed,n=len(y),max_absolute_error=float(np.max(np.abs(values-old.prediction)))))
        base=p.metrics(y,np.mean(seed_values,axis=0),high)
        if maps is None:
            maps,plan=make_maps(rows.target_date)
            np.savez_compressed(ROOT/'evidence/permutation_indices.npz',**maps)
            p.write_json(ROOT/'evidence/permutation_plan.json',plan)
            diagnostics=[]
            for name,indices in maps.items():
                for repeat,index in enumerate(indices):
                    distance=np.abs(index-np.arange(len(y)))
                    diagnostics.append(dict(setting=name,repeat=repeat,changed_fraction=float(np.mean(distance>0)),
                      mean_absolute_displacement_days=float(distance.mean()),
                      same_month_fraction=float(np.mean(rows.target_date.dt.month.to_numpy()[index]==rows.target_date.dt.month.to_numpy()))))
            pd.DataFrame(diagnostics).to_csv(ROOT/'evidence/perturbation_diagnostics.csv',index=False)
        fast=None;all_map_fast=None;errors=[]
        if record.model=='SVM_RBF':
            from rbf_acceleration import make
            all_map_fast,errors=make(m,predict,x,maps,rows.target_date)
        elif record.model in ['BayesianRidge','Poisson','Tweedie']: fast,errors=linear_disruptor(m,predict,x)
        elif record.model in ['RandomForest','ExtraTrees']:
            from forest_paths import make
            all_map_fast,errors=make(m,predict,x,maps)
        elif record.model=='LightGBM':
            from lightgbm_paths import make
            all_map_fast,errors=make(m,predict,x,maps)
        else:
            from repeated_input_cache import make
            all_map_fast=make(predict,x,maps,np.mean(seed_values,axis=0))
        p.write_json(ROOT/'evidence'/f'{slug}__{record.model}__audit.json',dict(unit=record.unit,model=record.model,
          baseline=base,seed_replay=seed_checks,exact_optimization_check_errors=errors,threshold=meta['threshold'],
          n=2557,high_n=int(high.sum()),columns=list(x.columns),protocol_sha256=digest))
        all_columns_cache={}
        for setting,_,_ in SETTINGS:
            destination=destinations[setting]
            if destination.exists() and destination.with_suffix('.complete.json').exists():
                done=json.loads(destination.with_suffix('.complete.json').read_text(encoding='utf-8'))
                assert done['protocol_sha256']==digest and p.sha(destination)==done['sha256']
                continue
            entries=[];part_start=time.perf_counter()
            # Four variants per batch bounds dense neural activation memory.
            descriptors=list(itertools.product(list(x.columns),range(REPEATS)))
            for offset in range(0,len(descriptors),4):
                group=descriptors[offset:offset+4]
                if all_map_fast is not None:
                    outputs=[]
                    for column,repeat in group:
                        if column not in all_columns_cache:
                            all_columns_cache[column]=all_map_fast(column)
                        outputs.append(all_columns_cache[column][setting][repeat])
                elif fast is not None:
                    outputs=[fast(column,maps[setting][repeat]) for column,repeat in group]
                else:
                    variants=[]
                    for column,repeat in group:
                        variant=x.copy();variant[column]=x[column].to_numpy()[maps[setting][repeat]]
                        variants.append(variant)
                    outputs=predict(pd.concat(variants,ignore_index=True)).reshape(len(group),len(y))
                for (column,repeat),values in zip(group,outputs):
                    scores=p.metrics(y,values,high)
                    entry=dict(setting=setting,unit=record.unit,model=record.model,feature=column,
                      label=p.feature_label(column),family=p.family(column),repeat=repeat,n=len(y),high_n=int(high.sum()))
                    for metric,value in scores.items():
                        entry[f'baseline_{metric}']=base[metric];entry[f'perturbed_{metric}']=value
                        entry[f'delta_{metric}']=base[metric]-value if metric=='r2' else value-base[metric]
                    assert all(np.isfinite(v) for k,v in entry.items() if k.startswith(('baseline_','perturbed_','delta_')))
                    entries.append(entry)
                if offset%160==0:
                    print(f'RUN {number+1}/91 {record.unit}/{record.model}/{setting}: {offset+len(group)}/810 scores; {time.perf_counter()-part_start:.1f}s',flush=True)
            assert np.array_equal(x.to_numpy(),original)
            pd.DataFrame(entries).to_csv(destination,index=False)
            p.write_json(destination.with_suffix('.complete.json'),dict(protocol_sha256=digest,
              sha256=p.sha(destination),rows=len(entries),seconds=time.perf_counter()-part_start))
            print(f'COMPLETE {number+1}/91 {record.unit}/{record.model}/{setting}: {time.perf_counter()-part_start:.1f}s',flush=True)
        if all_map_fast is not None and hasattr(all_map_fast,'statistics'):
            pd.DataFrame(all_map_fast.statistics).to_csv(ROOT/'evidence'/f'{slug}__{record.model}__inference_cache.csv',index=False)
        del predict,seed_values,fast,all_map_fast,all_columns_cache
        gc.collect()
        print(f'BUNDLE {number+1}/91 done; total elapsed {time.perf_counter()-all_start:.1f}s',flush=True)
    print('ALL INFERENCE COMPLETE',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Full-record frozen-model individual-feature diagnostic. No estimator fitting. Requires authorized external snapshots and preflight cache.')
    parser.add_argument('--check-inputs',action='store_true',help='Check configured artifact locations only, without model loading or inference')
    args=parser.parse_args()
    paths=local_paths()
    if not paths.get('preflight') or not paths.get('experiment'):
        parser.error('Configure preflight and experiment in .local_paths.json before inference')
    if args.check_inputs:
        assert (Path(paths['preflight'])/'frames.pkl').is_file()
        bundles=list((Path(paths['experiment'])/'procedures/main').glob('*/S5/*/bundle.json'))
        assert len(bundles)==91
        print('Configured frozen input paths exist; 91 main S5 bundles. No inference or fitting performed.')
    else:
        with threadpool_limits(limits=4): run()
