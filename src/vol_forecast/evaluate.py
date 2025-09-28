from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Tuple

def rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def mae(y_true: pd.Series, y_pred: pd.Series) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))

def rolling_forecast_metrics(y: pd.Series, forecaster, window: int = 120) -> Tuple[float,float]:
    preds = []
    test = []
    for i in range(window, len(y)-1):
        train = y.iloc[i-window:i]
        model = forecaster(train)
        pred = getattr(model, 'predict', None)
        if pred is None:
            # statsmodels AutoReg has predict
            yhat = model.forecast(1).iloc[0]
        else:
            # arch model has forecast with variance
            f = model.forecast(horizon=1)
            if hasattr(f, 'variance'):
                yhat = float(np.sqrt(f.variance.iloc[-1,0]))
            else:
                yhat = float(f.mean.iloc[-1,0])
        preds.append(yhat)
        test.append(y.iloc[i+1])
    return rmse(np.array(test), np.array(preds)), mae(np.array(test), np.array(preds))
