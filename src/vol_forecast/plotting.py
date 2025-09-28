import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf

def timeseries(series: pd.Series, title: str, path: str):
    plt.figure(figsize=(10,4))
    series.plot()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

def acf_plot(series: pd.Series, lags: int, title: str, path: str):
    plt.figure(figsize=(8,4))
    plot_acf(series.dropna(), lags=lags)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
