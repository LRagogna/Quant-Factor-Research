import yfinance as yf
from pathlib import Path

#create path to store ticker info in data folder
project_root = Path(__file__).parent.parent
data_folder = project_root / "data"

#stocks for factor analysis
tickers = ["AAPL",
           "AMZN",
           "NVDA",
           "MSFT",
           "META"
           ]

#create tickers and export data -> data folder
for symbol in tickers:
    ticker = yf.Ticker(symbol)
    data = ticker.history(
        start = "2015-01-01",
        end = "2026-01-01")
    data.to_csv(data_folder / f"{symbol}.csv")