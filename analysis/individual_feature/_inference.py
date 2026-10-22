"""Read-only loading of trusted frozen procedure snapshots."""
from pathlib import Path
import os, sys, json, hashlib, pickle, pickletools, importlib.util
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from release_io import ROOT as REPO, local_paths
ROOT = REPO / 'generated/individual_feature'
ROOT.mkdir(parents=True, exist_ok=True)
_paths = local_paths() if (REPO / '.local_paths.json').exists() else {'preflight': '', 'experiment': ''}
FRAMES = Path(_paths['preflight']) / 'frames.pkl'
EXPERIMENT = Path(_paths['experiment'])

def load_helpers():
    import main_scheme as module
    def forbidden(*args, **kwargs):
        raise RuntimeError('Fitting is prohibited during this frozen-model diagnostic')
    for name in ['Pipeline','KerasMLPRegressor','RandomForestRegressor','ExtraTreesRegressor','BayesianRidge','PoissonRegressor','TweedieRegressor','SVR','KNeighborsRegressor']:
        if hasattr(module, name): getattr(module, name).fit = forbidden
    return module

def file_inventory():
    files = [FRAMES, EXPERIMENT/'configuration.json', REPO/'src/main_scheme.py']
    files += sorted((EXPERIMENT/'procedures/main').glob('*/S5/*/bundle.json'))
    return {str(path): sha(path) for path in files}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()

def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, default=str),encoding='utf-8')

def get_predictor(m, folder):
    meta=m.json_read(folder/'bundle.json')
    estimators=[]
    for seed in meta['seeds']:
        p=folder/f'seed_{seed}'
        done=m.json_read(p/'completed.json')
        for name, expected in done['files'].items():
            if sha(p/name)!=expected: raise ValueError(f'Seed digest mismatch: {p/name}')
        try:
            model=m.load_estimator(p)
        except Exception as error:
            if meta['candidate']['name']!='XGBoost': raise
            # Recover the unmodified native model payload from XGBoost's own
            # UBJSON memory snapshot. Training config is not needed for inference.
            import xgboost as xgb
            arrays=[bytes(arg) for op,arg,pos in pickletools.genops((p/'estimator.pkl').read_bytes()) if op.name=='BYTEARRAY8' and len(arg)>10000]
            if len(arrays)!=1: raise RuntimeError('Ambiguous XGBoost snapshot') from error
            key=b'L'+(5).to_bytes(8,'big')+b'Model'
            data=arrays[0]
            if data.count(key)!=1 or not data.endswith(b'}}'): raise RuntimeError('Unexpected XGBoost snapshot structure') from error
            payload=data[data.index(key)+len(key):-1]
            booster=xgb.Booster(); booster.load_model(bytearray(payload)); booster.set_param({'nthread':4})
            assert booster.num_features()==len(meta['columns'])
            class NativeXGBoost:
                def __init__(self,b): self.booster=b
                def predict(self,x): return self.booster.inplace_predict(x)
            model=NativeXGBoost(booster)
            recovered=ROOT/'evidence/recovered_xgboost'; recovered.mkdir(exist_ok=True)
            dest=recovered/f'{folder.parts[-3]}_seed_{seed}.ubj'
            dest.write_bytes(payload)
            write_json(dest.with_suffix('.json'),dict(source=str(p/'estimator.pkl'),source_sha256=sha(p/'estimator.pkl'),payload_sha256=sha(dest),payload_offset=data.index(key)+len(key),payload_bytes=len(payload),recovery='Byte-exact embedded XGBoost-produced Model subtree; no tree, threshold or objective changes',original_error=str(error)))
        # Restrict inference parallelism without changing fitted parameters.
        for obj in [model,*getattr(model,'named_steps',{}).values()]:
            if hasattr(obj,'n_jobs'): obj.n_jobs=4
        decision=m.json_read(p/'decision.json')
        estimators.append((seed,model,decision))
    direct=meta['candidate'].get('family') in ('poisson','tweedie')
    def predictions(x, per_seed=False):
        values=[]
        for seed,estimator,decision in estimators:
            raw=np.asarray(estimator.predict(x),dtype=float).reshape(-1)
            out=np.maximum(raw,0.) if direct else m.inverse_log1p_smearing(raw,decision['effective_factor'])
            if not np.isfinite(out).all(): raise ValueError('Nonfinite prediction')
            values.append(out)
        return values if per_seed else np.mean(values,axis=0)
    predictions.estimators=estimators
    return meta, predictions

def feature_label(name):
    if name.startswith('y_lag_'): return f'Log hotspot count, lag {name.rsplit("_",1)[1]} day(s)'
    if name.startswith('y_roll'):
        stat,days=name[6:].rsplit('_',1)
        return f'Previous {days}-day log hotspot {stat}'
    if name.startswith('rain_rollsum_'): return f'Rainfall, {name.rsplit("_",1)[1]}-day sum through target day'
    labels={'hth':'Dry-spell duration (DS)','rain':'Rainfall','evap':'Signed evaporation','wind':'Wind speed','iod':'IOD','nino':'Nino 3.4','mjo_amp':'MJO amplitude','romi1':'ROMI1','romi2':'ROMI2'}
    if '_lag_' in name:
        prefix,lag=name.rsplit('_lag_',1)
        return f'{labels[prefix]}, lag {lag} day(s)'
    return {'month_sin':'Month sine','month_cos':'Month cosine','doy_sin':'Day-of-year sine','doy_cos':'Day-of-year cosine'}[name]

def family(name):
    if name.startswith('y_'): return 'Hotspot history'
    if name.startswith('hth_'): return 'Dry-spell duration'
    if name.startswith('rain_'): return 'Rainfall'
    if name.startswith('evap_'): return 'Signed evaporation'
    if name.startswith('wind_'): return 'Wind speed'
    if name.startswith('iod_'): return 'IOD'
    if name.startswith('nino_'): return 'Nino 3.4'
    if name.startswith('mjo_amp_'): return 'MJO amplitude'
    if name.startswith('romi1_'): return 'ROMI1'
    if name.startswith('romi2_'): return 'ROMI2'
    return 'Calendar'

def metrics(y,p,high,weights=None):
    e=p-y
    w=np.ones(len(y)) if weights is None else weights
    mean_y=np.average(y,weights=w)
    return {'rmse':float(np.sqrt(np.average(e*e,weights=w))),'mae':float(np.average(np.abs(e),weights=w)),
            'rmse90':float(np.sqrt(np.average(e[high]**2,weights=w[high]))) if high.any() else np.nan,
            'mae90':float(np.average(np.abs(e[high]),weights=w[high])) if high.any() else np.nan,
            'r2':float(1-np.sum(w*e*e)/np.sum(w*(y-mean_y)**2))}
