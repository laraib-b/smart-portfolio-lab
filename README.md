# Smart Portfolio Lab

Traditional portfolio optimization (Project 1) — construct and evaluate equal-weight, minimum-variance, and maximum-Sharpe portfolios using historical US equities, then compare them out of sample against SPY.

## Status

Early progress (Milestone 1 started):

- Project layout, virtualenv, and dependencies
- Adjusted close price cache for 9 stocks + SPY (2020 → latest)
- Data exploration notebook: load prices, returns, correlation

Still to come: baseline portfolio, optimizers, efficient frontier, backtesting, experiments.

## Universe

`AAPL`, `MSFT`, `NVDA`, `AMZN`, `KO`, `WMT`, `JPM`, `XOM`, `JNJ`, benchmark `SPY`.

## Setup

```powershell
cd smart-portfolio-lab
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

In Cursor / VS Code, open notebooks under `notebooks/` and select the `.venv` kernel (`Python (smart-portfolio-lab)`).

## Run the first notebook

Open `notebooks/01_data_exploration.ipynb` and run all cells.

By default it loads `data/cache/prices_close.csv` (no live Yahoo call). To refresh from Yahoo Finance, set `refresh=True` in the load cell. Downloads can time out; retries help.

## Layout

```
smart-portfolio-lab/
  README.md
  requirements.txt
  src/
    data_loader.py
  notebooks/
    01_data_exploration.ipynb
  data/cache/
    prices_close.csv
  results/
```

## Disclaimer

Learning / research only. Not investment advice.
