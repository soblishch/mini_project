import yfinance as yf
import pandas as pd

ticker = "KER.WA"

data = yf.download(ticker, start='2025-07-19', end='2026-07-19', interval="1d")


data.columns = data.columns.droplevel(1)

data = data.dropna()

# зміна з 0 на 1, то ми купуємо акцію
# якщо є послідовність з 1, то ми тримаємо акцію
# якщо зміна з 1 на 0, то ми продаємо акцію

short_ma = 20
long_ma = 50

data["Moving average - 20"] = data["Close"].rolling(short_ma).mean()
data["Moving average - 50"] = data["Close"].rolling(long_ma).mean()

data["Signal"] = 0
for date in data.index:
    if data.loc[date, "Moving average - 20"] > data.loc[date, "Moving average - 50"]:
        data.loc[date, "Signal"] = 1

print(data)