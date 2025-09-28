from __future__ import annotations
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from arch import arch_model

def realized_volatility(returns: pd.Series, period: str = 'M') -> pd.Series:
    agg = returns.resample(period).std() * np.sqrt(21)
    return agg.dropna()

def fit_ar1_vol(vol: pd.Series):
    model = AutoReg(vol, lags=1, old_names=False).fit()
    return model

def fit_garch(returns: pd.Series):
    am = arch_model(returns.dropna(), mean='Constant', vol='Garch', p=1, q=1, dist='normal')
    res = am.fit(disp='off')
    return res

def fit_gjr_garch(returns: pd.Series):
    am = arch_model(returns.dropna(), mean='Constant', vol='GJR-GARCH', p=1, q=1, o=1, dist='normal')
    res = am.fit(disp='off')
    return res

def forecast_volatility(fitted, horizon: int = 1) -> pd.Series:
    f = fitted.forecast(horizon=horizon)
    if hasattr(f, 'variance'):
        v = f.variance.iloc[-1]
        out = np.sqrt(v)
        out.name = 'sigma_forecast'
        return out
    else:
        # statsmodels AutoReg
        return f.predicted_mean
