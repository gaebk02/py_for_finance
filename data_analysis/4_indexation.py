# 지수화 Indexation
# 누적곱과 지수화의 차이점
# 누적곱은 실질적인 수익률을 확인, 지수화는 여러 자산의 상대적인 성과를 비교.
# 주가를 100으로 지수화하여 비교하는 방법

import yfinance as yf
import matplotlib.pyplot as plt

kospi = yf.Ticker('^KS11').history(start='2000-01-04')
snp = yf.Ticker('^GSPC').history(start='2000-01-04')
kospi_index = (kospi['Close'] / kospi['Close'].loc['2000-01-04']) * 100
snp_index = (snp['Close'] / snp['Close'].loc['2000-01-04']) * 100

plt.figure(figsize=(9, 7)) # 그래프 크기 설정
plt.plot(kospi_index.index, kospi_index, 'b', label='KOSPI')
plt.plot(snp_index.index, snp_index, 'r', label='S&P500')
plt.grid(True)
plt.legend(loc='best')
plt.show()
