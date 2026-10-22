"""Exact RBF factorization, reusing within-year donor values across maps."""
import numpy as np

def make(m,predict,x,maps,dates):
    assert len(predict.estimators)==1
    _,pipe,decision=predict.estimators[0]
    scaler=pipe.named_steps['scaler'];model=pipe.named_steps['model']
    assert model.kernel=='rbf'
    z=scaler.transform(x);sv=model.support_vectors_;dual=model.dual_coef_.reshape(-1)
    d=(z*z).sum(axis=1)[:,None]+(sv*sv).sum(axis=1)[None,:]-2*z@sv.T
    settings=list(maps)
    combined=np.concatenate([maps[s] for s in settings],axis=0)
    years=np.asarray(dates.dt.year);gamma=model._gamma
    def column_all(column):
        j=x.columns.get_loc(column)
        raw=np.empty((len(combined),len(x)),dtype=np.float64)
        for year in sorted(set(years)):
            rows=np.flatnonzero(years==year)
            unique,codes=np.unique(z[rows,j],return_inverse=True)
            donor_code=np.full(len(x),-1,dtype=int);donor_code[rows]=codes
            remainder=d[rows]-(z[rows,j,None]-sv[None,:,j])**2
            if remainder.min() < -1e-7:raise ValueError('Invalid RBF remaining distance')
            # K(x,sv)=K_without_column(x,sv)*K_column(new_value,sv).
            # Matrix multiplication sums the identical retained dual expansion.
            without=np.exp(-gamma*np.maximum(remainder,0))*dual[None,:]
            kernel_column=np.exp(-gamma*(unique[:,None]-sv[None,:,j])**2)
            grid=without@kernel_column.T+model.intercept_[0]
            ids=donor_code[combined[:,rows]]
            assert (ids>=0).all()
            raw[:,rows]=grid[np.arange(len(rows))[None,:],ids]
        values=m.inverse_log1p_smearing(raw,decision['effective_factor'])
        return {s:values[i*10:(i+1)*10] for i,s in enumerate(settings)}
    errors=[]
    for column in ['y_lag_1','hth_lag_0','iod_lag_0','doy_sin']:
        values=column_all(column)
        for setting in maps:
            altered=x.copy();altered[column]=x[column].to_numpy()[maps[setting][0]]
            exact=predict(altered);fast=values[setting][0]
            errors.append(float(np.max(np.abs(exact-fast))))
            if not np.allclose(exact,fast,rtol=1e-9,atol=1e-8):
                raise ValueError(f'RBF factorization failed {column}/{setting}: {errors[-1]}')
    return column_all,errors
