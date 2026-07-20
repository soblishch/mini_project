import yfinance as yf
import pandas as pd

ticker = "KER.WA"

data = yf.download(ticker, start='2025-07-19', end='2026-07-19', interval="1d")
data.columns = data.columns.droplevel(1)

data = data.dropna()

print(data)
