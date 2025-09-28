from pathlib import Path
import pandas as pd
from vol_forecast.data import load_prices, daily_log_returns
from vol_forecast.modeling import realized_volatility, fit_ar1_vol, fit_garch, fit_gjr_garch, forecast_volatility
from vol_forecast.evaluate import rolling_forecast_metrics
from vol_forecast import plotting

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'
FIGS = REPORTS / 'figures'
FIGS.mkdir(parents=True, exist_ok=True)

def main():
    prices = load_prices(DATA/'sp500.csv', DATA/'ge.csv', use_download=True)

    sp = prices['SP500']['price']
    ge = prices['GE']['price']

    r_sp = daily_log_returns(sp)
    r_ge = daily_log_returns(ge)

    v_sp_m = realized_volatility(r_sp, 'M')
    v_ge_m = realized_volatility(r_ge, 'M')

    plotting.timeseries(v_sp_m, 'SP500 monthly realized volatility', str(FIGS/'sp500_vol_m.png'))
    plotting.timeseries(v_ge_m, 'GE monthly realized volatility', str(FIGS/'ge_vol_m.png'))

    ar_sp = fit_ar1_vol(v_sp_m)
    ar_ge = fit_ar1_vol(v_ge_m)

    garch_sp = fit_garch(r_sp.resample('M').last())
    garch_ge = fit_garch(r_ge.resample('M').last())

    gjr_sp = fit_gjr_garch(r_sp.resample('M').last())
    gjr_ge = fit_gjr_garch(r_ge.resample('M').last())

    # quick forecast demo
    f_ar_sp = ar_sp.forecast(1).iloc[-1]
    f_ar_ge = ar_ge.forecast(1).iloc[-1]

    f_garch_sp = forecast_volatility(garch_sp, 1).iloc[0]
    f_garch_ge = forecast_volatility(garch_ge, 1).iloc[0]

    with open(REPORTS/'summary.md', 'w') as f:
        f.write('AutoReg one step ahead forecast SP500: ' + str(round(float(f_ar_sp), 4)) + '\n')
        f.write('AutoReg one step ahead forecast GE: ' + str(round(float(f_ar_ge), 4)) + '\n')
        f.write('GARCH one step ahead forecast SP500: ' + str(round(float(f_garch_sp), 4)) + '\n')
        f.write('GARCH one step ahead forecast GE: ' + str(round(float(f_garch_ge), 4)) + '\n')

if __name__ == '__main__':
    main()
