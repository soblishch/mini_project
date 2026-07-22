import yfinance as yf
import matplotlib.pyplot as plt

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



# P/L
buy_price = 0
profit_lost = []

for i in range(len(data)):
    if i == 0:
        profit_lost.append(0)
        continue

    if data["Signal"].iloc[i] == 1 and data["Signal"].iloc[i-1] == 0:
        buy_price = data["Close"].iloc[i]
        profit_lost.append(0)
    elif data["Signal"].iloc[i] == 1 and data["Signal"].iloc[i-1] == 1:
        profit = data["Close"].iloc[i] - data["Close"].iloc[i - 1]
        profit_lost.append(profit)
    elif data["Signal"].iloc[i] == 0 and data["Signal"].iloc[i - 1] == 1:
        profit = data["Close"].iloc[i] - data["Close"].iloc[i - 1]
        profit_lost.append(profit)
    else:
        profit_lost.append(0)

data["Profit/Lost"] = profit_lost


data.to_csv("data.csv", encoding="utf-8")

print(f"Profit: {data["Profit/Lost"].sum()}")



#Візуалізація

plt.ylabel("Ціна")
plt.xlabel("Дата")

plt.plot(data.index, data["Close"])

plt.show()