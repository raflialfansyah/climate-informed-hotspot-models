"""Exact additive LightGBM regression trees, with numerical-split-only guard."""
import numpy as np
from numba import set_num_threads
from forest_paths import path_masks,evaluate

def make(m,predict,x,maps):
    set_num_threads(4)
    names=list(maps);indices=np.concatenate([maps[name] for name in names],axis=0)
    models=[]
    for _,pipe,decision in predict.estimators:
        model=pipe.named_steps['model'] if hasattr(pipe,'named_steps') else pipe
        scaler=pipe.named_steps.get('scaler') if hasattr(pipe,'named_steps') else None
        z=np.ascontiguousarray(scaler.transform(x) if scaler is not None else x.to_numpy(),dtype=np.float64)
        dump=model.booster_.dump_model()
        assert dump['num_tree_per_iteration']==1 and dump['average_output'] is False
        assert dump['objective'].startswith('regression')
        assert model.best_iteration_<=0 or model.best_iteration_==len(dump['tree_info'])
        starts=[];left=[];right=[];feature=[];threshold=[];value=[];max_depth=[0]
        def visit(node,depth):
            idx=len(left);left.append(-1);right.append(-1);feature.append(-2);threshold.append(-2.);value.append(0.)
            max_depth[0]=max(max_depth[0],depth)
            if 'leaf_value' in node:
                value[idx]=node['leaf_value'];return idx
            assert node['decision_type']=='<='
            assert node.get('missing_type') in ('None','NaN')
            feature[idx]=node['split_feature'];threshold[idx]=float(node['threshold'])
            left[idx]=visit(node['left_child'],depth+1)
            right[idx]=visit(node['right_child'],depth+1)
            return idx
        for tree in dump['tree_info']:starts.append(visit(tree['tree_structure'],0))
        arrays=(np.asarray(starts,dtype=np.int64),np.asarray(left,dtype=np.int64),np.asarray(right,dtype=np.int64),
          np.asarray(feature,dtype=np.int64),np.asarray(threshold,dtype=np.float64),np.asarray(value,dtype=np.float64))
        baseline=np.asarray(pipe.predict(x),dtype=float)
        masks=path_masks(z,*arrays[:5])
        models.append((z,arrays,max_depth[0]+3,baseline,decision,masks))
    def column_all(column):
        j=x.columns.get_loc(column);out=[]
        for z,arrays,capacity,baseline,decision,masks in models:
            donor=np.ascontiguousarray(z[indices,j])
            raw=evaluate(z,j,donor,baseline,*arrays,capacity,*masks,1.)
            out.append(m.inverse_log1p_smearing(raw,decision['effective_factor']))
        result=np.mean(out,axis=0)
        return {name:result[i*10:(i+1)*10] for i,name in enumerate(names)}
    errors=[]
    for column in ['y_lag_1','hth_lag_0','iod_lag_0','doy_sin']:
        values=column_all(column)
        for name in maps:
            changed=x.copy();changed[column]=x[column].to_numpy()[maps[name][0]]
            exact=predict(changed);fast=values[name][0]
            error=float(np.max(np.abs(exact-fast)));errors.append(error)
            if not np.allclose(exact,fast,rtol=1e-9,atol=1e-8):
                raise ValueError(f'LightGBM path intervals failed {column}/{name}: {error}')
    return column_all,errors
