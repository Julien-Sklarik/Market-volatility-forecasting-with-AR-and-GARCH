import pandas as pd
import numpy as np
from pathlib import Path

def _read_local_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if 'date' not in df.columns:
        raise ValueError(f"CSV at {path} must have a date column")
    if 'price' not in df.columns and 'PRC' in df.columns and 'CFACPR' in df.columns:
        df = df.copy()
        df['price'] = df['PRC'] / df['CFACPR']
    if 'price' not in df.columns:
        raise ValueError(f"CSV at {path} must have a price column")
    df['date'] = pd.to_datetime(df['date'])
    df = df[['date','price']].dropna()
    df = df.sort_values('date').set_index('date')
    return df

def _try_download(ticker: str) -> pd.DataFrame:
    try:
        import yfinance as yf
    except Exception:
        raise RuntimeError("yfinance not installed and local data missing")
    data = yf.download(ticker, progress=False)
    if data.empty:
        raise RuntimeError(f"could not download data for {ticker}")
    out = data[['Adj Close']].rename(columns={'Adj Close':'price'})
    out.index.name = 'date'
    return out

def load_prices(sp_path: Path, ge_path: Path, use_download: bool = True) -> dict:
    res = {}
    if sp_path.exists():
        res['SP500'] = _read_local_csv(sp_path)
    elif use_download:
        res['SP500'] = _try_download('SPY')
    else:
        raise FileNotFoundError(f"{sp_path} not found")

    if ge_path.exists():
        res['GE'] = _read_local_csv(ge_path)
    elif use_download:
        res['GE'] = _try_download('GE')
    else:
        raise FileNotFoundError(f"{ge_path} not found")
    return res

def daily_log_returns(price: pd.Series) -> pd.Series:
    ret = 100 * np.log(price / price.shift(1))
    return ret.dropna()
