# 종가 차트

import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt


aapl = yf.Ticker('AAPL').history(start='2024-11-01')
aapl.dropna()

plt.figure(figsize=(10, 6))
plt.title('AAPL Candle Chart')
plt.plot(range(len(aapl)), aapl['Close'], 'co-', label='Close')
plt.grid(color='gray', linestyle='--')

plt.xticks(
    ticks=range(len(aapl)),
    labels=aapl.index.strftime('%Y-%m-%d'),
    rotation=45, # 45도 회전
    fontsize=8
)
plt.show()
