# 최대 손실 낙폭 Maximum Drawdown
# 최고점에서 최저점까지의 가장 큰 손실 / 손실을 취소화하는 퀀트 투자에서는 mdd를 가장 중요시 하는 것이 좋다고도 한다.

import yfinance as yf
import matplotlib.pyplot as plt

snp = yf.Ticker('^GSPC').history(start='2005-01-01')

window = 252 # 1년을 252일로 설정
peak = snp['Close'].rolling(window, min_periods=1).max() # 최고점, rolling은 252일 데이터 중 1일부터 최대값을 구함
drawdown = snp['Close'] / peak - 1.0 # 최대 손실 낙폭
max_dd = drawdown.rolling(window, min_periods=1).min() # 최대 손실 낙폭의 최소값

plt.figure(figsize=(9, 7)) # 그래프 크기 설정
plt.subplot(211) # 2행 1열 중 1행에 그래프 생성
snp['Close'].plot(label='S&P500', title='S&P500 MDD', grid=True, legend=True)
plt.subplot(212) # 2행 1열 중 2행에 그래프 생성
drawdown.plot(c='b', label='Drawdown', grid=True, legend=True)
max_dd.plot(c='r', label='Max Drawdown', grid=True, legend=True)
plt.show()

mxa_dd_peak = max_dd.min() # 최대 손실 낙폭의 최소값
mxx_dd[max_dd == max_dd.min()] # 최대 손실 낙폭의 최소값이 나타나는 날짜
