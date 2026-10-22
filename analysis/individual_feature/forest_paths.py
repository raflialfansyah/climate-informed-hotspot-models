"""Exact frozen forest path intervals for all 40 single-column donor maps.

For fixed other columns, each tree is a piecewise-constant function of the
changed column. Traverse both sides of its splits, and follow only the fixed
side for every other split. This reuses identical paths across donor maps.
"""
import numpy as np
from numba import njit,prange,set_num_threads

@njit(cache=True,parallel=True)
def path_masks(z,starts,left,right,features,threshold):
    n=len(z);nt=len(starts)
    low=np.zeros((n,nt),dtype=np.uint64);high=np.zeros((n,nt),dtype=np.uint32)
    for row in prange(n):
        for tree in range(nt):
            node=starts[tree]
            while left[node]>=0:
                f=features[node]
                if f<64:low[row,tree]|=np.uint64(1)<<np.uint64(f)
                else:high[row,tree]|=np.uint32(1)<<np.uint32(f-64)
                node=left[node] if z[row,f]<=threshold[node] else right[node]
    return low,high

@njit(cache=True,parallel=True)
def evaluate(z,j,donors,baseline,starts,left,right,features,threshold,value,capacity,masklo,maskhi,denominator):
    reps,n=donors.shape
    result=np.empty((reps,n),dtype=np.float64)
    for row in prange(n):
        for rep in range(reps):result[rep,row]=baseline[row]
        nodes=np.empty(capacity,dtype=np.int64)
        lower=np.empty(capacity,dtype=np.float64)
        upper=np.empty(capacity,dtype=np.float64)
        vmin=np.min(donors[:,row]);vmax=np.max(donors[:,row])
        for tree in range(len(starts)):
            if j<64:
                if (masklo[row,tree]&(np.uint64(1)<<np.uint64(j)))==0:continue
            else:
                if (maskhi[row,tree]&(np.uint32(1)<<np.uint32(j-64)))==0:continue
            node=starts[tree];first=-1
            while left[node]>=0:
                f=features[node]
                if f==j and first<0:first=node
                node=left[node] if z[row,f]<=threshold[node] else right[node]
            if first<0:continue
            old=value[node]
            nodes[0]=first;lower[0]=-np.inf;upper[0]=np.inf;size=1
            while size>0:
                size-=1;node=nodes[size];lo=lower[size];hi=upper[size]
                while left[node]>=0 and features[node]!=j:
                    f=features[node]
                    node=left[node] if z[row,f]<=threshold[node] else right[node]
                if left[node]<0:
                    change=(value[node]-old)/denominator
                    if change!=0:
                        for rep in range(reps):
                            if donors[rep,row]>lo and donors[rep,row]<=hi:result[rep,row]+=change
                else:
                    split=threshold[node]
                    left_hi=min(hi,split)
                    if left_hi>=vmin and lo<vmax and lo<left_hi:
                        nodes[size]=left[node];lower[size]=lo;upper[size]=left_hi;size+=1
                    right_lo=max(lo,split)
                    if hi>=vmin and right_lo<vmax and right_lo<hi:
                        nodes[size]=right[node];lower[size]=right_lo;upper[size]=hi;size+=1
    return result

def make(m,predict,x,maps):
    set_num_threads(4)
    settings=list(maps);indices=np.concatenate([maps[s] for s in settings],axis=0)
    estimators=[]
    for _,pipe,decision in predict.estimators:
        forest=pipe.named_steps['model'] if hasattr(pipe,'named_steps') else pipe
        scaler=pipe.named_steps.get('scaler') if hasattr(pipe,'named_steps') else None
        assert forest.__class__.__name__ in ('RandomForestRegressor','ExtraTreesRegressor') and forest.n_outputs_==1
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
        capacity=max(e.tree_.max_depth for e in forest.estimators_)+3
        baseline=np.asarray(pipe.predict(x),dtype=float)
        masks=path_masks(z,*arrays[:5])
        estimators.append((z,arrays,capacity,baseline,decision,masks))
    def column_all(column):
        j=x.columns.get_loc(column);out=[]
        for z,arrays,capacity,baseline,decision,masks in estimators:
            donor=np.ascontiguousarray(z[indices,j])
            raw=evaluate(z,j,donor,baseline,*arrays,capacity,*masks,len(arrays[0]))
            out.append(m.inverse_log1p_smearing(raw,decision['effective_factor']))
        values=np.mean(out,axis=0)
        return {s:values[i*10:(i+1)*10] for i,s in enumerate(settings)}
    errors=[]
    for column in ['y_lag_1','hth_lag_0','iod_lag_0','doy_sin']:
        values=column_all(column)
        for setting in maps:
            altered=x.copy();altered[column]=x[column].to_numpy()[maps[setting][0]]
            exact=predict(altered);fast=values[setting][0]
            error=float(np.max(np.abs(exact-fast)));errors.append(error)
            if not np.allclose(exact,fast,rtol=1e-10,atol=1e-8):
                raise ValueError(f'Forest path intervals failed {column}/{setting}: {error}')
    return column_all,errors
