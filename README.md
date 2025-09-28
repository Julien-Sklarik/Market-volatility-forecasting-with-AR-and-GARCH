# Market volatility forecasting with AR and GARCH

This project demonstrates a compact end to end workflow that a quant can run on fresh equity data to study and forecast volatility. The focus is on SP500 and GE with fully reproducible code organized as a small python package plus a light pipeline.

Highlights
1 Clean data api that loads local csv files or fetches from a public source if present
2 Classical models for volatility AR 1 GARCH 1 1 and GJR GARCH 1 1
3 Clear forecast evaluation with RMSE and MAE using rolling origin
4 Figures saved into reports that you can drop into a slide or portfolio
5 A tidy structure that reads as a real project not a class submission

Quick start
1 Create a fresh virtual environment
2 From the repo root run
   pip install .
3 Put two csv files in the data folder if you already have them
   data/sp500.csv
   data/ge.csv
   Each csv must have columns date and price
   The date column must parse as YYYY MM DD
   The price column is the close price adjusted for splits and dividends if possible
4 Run the pipeline
   python scripts/run_all.py
5 Review figures and metrics under reports

Data
You can supply your own csv files as noted above. If the files are missing the loader will try to download daily close prices for SPY as a proxy for the index and for GE using a public source. You may switch tickers in scripts or in src vol_forecast data.py

Methods
1 Convert daily close prices to daily log returns in percent
2 Aggregate to weekly and monthly horizons for volatility study
3 Fit AR 1 on realized volatility and GARCH 1 1 or GJR GARCH 1 1 on returns
4 Produce one step ahead forecasts with a rolling window
5 Score forecasts with RMSE and MAE

Selected results
The figures below are extracted from the notebook you provided and saved into the project so the repo looks complete even before you run it on your machine.

![Figure 1](reports/figures/figure_01.png)
![Figure 2](reports/figures/figure_02.png)
![Figure 3](reports/figures/figure_03.png)

Project layout
```
repo root
├── src
│   └── vol_forecast
│       ├── __init__.py
│       ├── data.py
│       ├── modeling.py
│       ├── evaluate.py
│       └── plotting.py
├── scripts
│   └── run_all.py
├── notebooks
│   ├── volatility_forecasting_walkthrough.ipynb
│   └── archive
│       └── berkeley_original_ps6_solution.ipynb
├── reports
│   ├── figures
│   │   ├── figure_01.png
│   │   ├── figure_02.png
│   │   ├── figure_03.png
│   │   ├── figure_04.png
│   │   ├── figure_05.png
│   │   ├── figure_06.png
│   │   └── figure_07.png
│   └── summary.md
├── data
│   └── README.md
├── tests
│   └── test_smoke.py
├── README.md
├── pyproject.toml
├── .gitignore
└── LICENSE
```

Notes
1 The notebook in notebooks volatility_forecasting_walkthrough.ipynb is a clean narrative version that calls the package functions and reproduces the key steps and plots
2 The archive folder preserves your original notebook for provenance
3 The python package name and module names use underscores throughout to keep naming clean for resumes and profiles
4 If you plan to show the repo in interviews include the three strongest figures in the README and pin a short description at the top of the repo page

