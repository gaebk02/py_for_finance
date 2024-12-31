## 산점도 Scatter Plot
## 독립변수 x와 종속변수 y 사이의 관계를 나타내는 그래프
## 가로축은 독립변수 x, 세로축은 종속변수 y
## 미국시장과 한국시장의 상관관계를 산점도로 확인, snp는 x축, kospi는 y축
## 점의 분포가 y = x인 직선 형태가 될 수록 직접적인 관계가 있음, 산점도만으로는 정확한 분석이 어려우므로 선형 회귀 분석을 통해 확인

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

kospi = yf.Ticker('^KS11').history(start='2000-01-04')
snp = yf.Ticker('^GSPC').history(start='2000-01-04')
# len(snp), len(kospi) # 데이터 길이 확인 / 개장일이 다르다보니, 두 길이가 다름

snp.index = snp.index.tz_convert('Asia/Seoul') # 한국 시간으로 변경(x축인 미국으로 지정해도 되나, 한국 일자로 알기 쉽게 변경)
df = pd.DataFrame({'snp': snp['Close'], 'kospi': kospi['Close']})
df.index = df.index.normalize() # 날짜를 일자만 표시
df = df.groupby(df.index).mean() # 공통화
df = df.fillna(method='bfill') # 빈 값 채우기 backword fill, NaN 값을 뒤의 값으로 채움
df = df.fillna(method='ffill') # 빈 값 채우기 forward fill, NaN 값을 앞의 값으로 채움

plt.scatter(df['snp'], df['kospi'], marker='.') # 산점도 생성
plt.xlabel('S&P500')
plt.ylabel('KOSPI')
plt.title('S&P500 vs KOSPI')
plt.grid(True)
plt.show()
