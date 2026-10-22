"""Exact frozen sklearn forest prediction under a single-column intervention.

Traverse each original path once. If the changed column was never visited,
the leaf is unchanged; otherwise resume at its first original path occurrence.
No tree, threshold, fitted value or input precision is altered.
"""
import numpy as np
from numba import njit

@njit(cache=True)
def evaluate(z,j,donor_values,starts,left,right,feature,threshold,value):
    reps,n=donor_values.shape
    result=np.zeros((reps,n),dtype=np.float64)
    for tree in range(len(starts)):
        root=starts[tree]
        for row in range(n):
            node=root;first=-1
            while left[node]>=0:
                f=feature[node]
                if f==j and first<0:first=node
                node=left[node] if z[row,f]<=threshold[node] else right[node]
            original=value[node]
            if first<0:
                for rep in range(reps):result[rep,row]+=original
            else:
                for rep in range(reps):
                    node=first
                    while left[node]>=0:
                        f=feature[node]
                        v=donor_values[rep,row] if f==j else z[row,f]
                        node=left[node] if v<=threshold[node] else right[node]
                    result[rep,row]+=value[node]
    return result/len(starts)

def make(m,predict,x,maps):
    estimators=[]
    for seed,pipe,decision in predict.estimators:
        forest=pipe.named_steps['model'] if hasattr(pipe,'named_steps') else pipe
        scaler=pipe.named_steps.get('scaler') if hasattr(pipe,'named_steps') else None
        assert forest.__class__.__name__ in ('RandomForestRegressor','ExtraTreesRegressor')
        assert forest.n_outputs_==1
        z=np.ascontiguousarray(scaler.transform(x) if scaler is not None else x.to_numpy(),dtype=np.float32)
        starts=[];left=[];right=[];features=[];thresholds=[];values=[];offset=0
        for estimator in forest.estimators_:
            tree=estimator.tree_;starts.append(offset)
            left.append(np.where(tree.children_left>=0,tree.children_left+offset,-1))
            right.append(np.where(tree.children_right>=0,tree.children_right+offset,-1))
            features.append(tree.feature);thresholds.append(tree.threshold)
            values.append(tree.value.reshape(-1));offset+=tree.node_count
        arrays=(np.asarray(starts,dtype=np.int64),np.concatenate(left),np.concatenate(right),
          np.concatenate(features),np.concatenate(thresholds),np.concatenate(values))
        estimators.append((z,arrays,decision))
    def predict_feature(column,setting):
        j=x.columns.get_loc(column);outputs=[]
        for z,arrays,decision in estimators:
            donors=np.ascontiguousarray(z[maps[setting],j])
            raw=evaluate(z,j,donors,*arrays)
            outputs.append(m.inverse_log1p_smearing(raw,decision['effective_factor']))
        return np.mean(outputs,axis=0)
    errors=[]
    # Check different column groups and all temporal settings on complete dates.
    for setting in maps:
        for column in ['y_lag_1','hth_lag_0','iod_lag_0','doy_sin']:
            fast=predict_feature(column,setting)[0]
            variant=x.copy();variant[column]=x[column].to_numpy()[maps[setting][0]]
            exact=predict(variant)
            error=float(np.max(np.abs(exact-fast)));errors.append(error)
            if not np.allclose(exact,fast,rtol=1e-10,atol=1e-8):
                raise ValueError(f'Forest acceleration failed: {column}/{setting}: {error}')
    return predict_feature,errors
