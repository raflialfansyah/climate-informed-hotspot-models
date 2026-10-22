"""Reuse original-estimator predictions only for exactly identical input rows."""
import time
import numpy as np

def make(predict,x,maps,baseline):
    names=list(maps);indices=np.concatenate([maps[name] for name in names],axis=0)
    n=len(x);target=np.tile(np.arange(n,dtype=np.int32),len(indices))
    stats=[]
    def column_all(column):
        start=time.perf_counter()
        values=x[column].to_numpy()[indices].reshape(-1)
        keys=np.empty(len(values),dtype=[('row','i4'),('value','f8')])
        keys['row']=target;keys['value']=values
        unique,inverse=np.unique(keys,return_inverse=True)
        # The inverse must recover both the exact original-row context and
        # the exact raw donor value. No rounding or approximate grouping.
        assert np.array_equal(unique['row'][inverse],target)
        assert np.array_equal(unique['value'][inverse],values)
        original=x[column].to_numpy()[unique['row']]
        unchanged=unique['value']==original
        predictions=np.empty(len(unique),dtype=float)
        predictions[unchanged]=baseline[unique['row'][unchanged]]
        changed=np.flatnonzero(~unchanged)
        for offset in range(0,len(changed),8192):
            subset=changed[offset:offset+8192]
            variant=x.iloc[unique['row'][subset]].copy()
            variant[column]=unique['value'][subset]
            predictions[subset]=predict(variant)
        out=predictions[inverse].reshape(indices.shape)
        stats.append(dict(feature=column,requested_rows=len(keys),unique_rows=len(unique),
          reused_unchanged_rows=int(unchanged.sum()),original_estimator_rows=len(changed),
          seconds=time.perf_counter()-start))
        return {name:out[i*10:(i+1)*10] for i,name in enumerate(names)}
    column_all.statistics=stats
    return column_all
