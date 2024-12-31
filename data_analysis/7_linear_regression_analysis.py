# 선형 회귀 분석 Linear Regression Analysis

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from spicy import stats # 선형 회귀 분석을 위한 라이브러리


# S&P500과 KOSPI의 선형 회귀 분석 결과를 산점도와 함께 시각화
kospi = yf.Ticker('^KS11').history(start='2000-01-04')
snp = yf.Ticker('^GSPC').history(start='2000-01-04')

snp.index = snp.index.tz_convert('Asia/Seoul') # 한국 시간으로 변경(x축인 미국으로 지정해도 되나, 한국 일자로 알기 쉽게 변경)
df = pd.DataFrame({'snp': snp['Close'], 'kospi': kospi['Close']})
df.index = df.index.normalize() # 날짜를 일자만 표시
df = df.groupby(df.index).mean() # 공통화
df = df.fillna(method='bfill') # 빈 값 채우기 backword fill, NaN 값을 뒤의 값으로 채움
df = df.fillna(method='ffill') # 빈 값 채우기 forward fill, NaN 값을 앞의 값으로 채움

regr = stats.linregress(df['snp'], df['kospi']) # 선형 회귀 분석
regr_line = f'KOSPI = {regr.slope:.2f} S&P500 + {regr.intercept:.2f}' # 선형 회귀식, slope: 기울기, intercept: y절편, .2f: 소수점 둘째자리까지 표시

plt.figure(figsize=(7, 7)) # 그래프 크기 설정
plt.plot(df['snp'], df['kospi'], '.') # 산점도 생성
plt.plot(df['snp'], regr.slope * df['snp'] + regr.intercept, 'r') # 선형 회귀선 생성
plt.legend(['S&P500 x KOSPI'], loc='best')
plt.title(f'S&P500 x KOSPI (R = {regr.rvalue:.2f})') # 상관계수 표시
plt.xlabel('S&P500')
plt.ylabel('KOSPI')
plt.show() # R = 0.78



# S&P500과 Dow지수의 선형 회귀 분석 결과를 산점도와 함께 시각화
dow = yf.Ticker('^DJI').history(start='2000-01-04')
snp = yf.Ticker('^GSPC').history(start='2000-01-04')
df = pd.DataFrame({'snp': snp['Close'], 'dow': dow['Close']})
df = df.fillna(method='bfill') # 빈 값 채우기 backword fill, NaN 값을 뒤의 값으로 채움
df = df.fillna(method='ffill') # 빈 값 채우기 forward fill, NaN 값을 앞의 값으로 채움

regr = stats.linregress(df['snp'], df['dow']) # 선형 회귀 분석
regr_line = f'Dow = {regr.slope:.2f} S&P500 + {regr.intercept:.2f}' # 선형 회귀식, slope: 기울기, intercept: y절편, .2f: 소수점 둘째자리까지 표시

plt.figure(figsize=(7, 7)) # 그래프 크기 설정
plt.plot(df['snp'], df['dow'], '.') # 산점도 생성
plt.plot(df['snp'], regr.slope * df['snp'] + regr.intercept, 'r') # 선형 회귀선 생성
plt.legend(['S&P500 x Dow'], loc='best')
plt.title(f'S&P500 x Dow (R = {regr.rvalue:.2f})') # 상관계수 표시
plt.xlabel('S&P500')
plt.ylabel('Dow')
plt.show() # R = 0.99, 두 지수의 상관관계가 매우 높음, 상관관계가 낮은 kospi와 snp의 경우가 리스크 완화효과가 높다고 볼 수 있음

# 메소드화
def linear_regression_analysis(x_ticker, y_ticker, start_date):
    x = yf.Ticker(x_ticker).history(start=start_date)
    y = yf.Ticker(y_ticker).history(start=start_date)
    x.index = x.index.tz_convert('Asia/Seoul')
    y.index = y.index.tz_convert('Asia/Seoul')
    df = pd.DataFrame({x_ticker: x['Close'], y_ticker: y['Close']})
    df.index = df.index.normalize()
    df = df.groupby(df.index).mean()
    df = df.fillna(method='bfill')
    df = df.fillna(method='ffill')
    regr = stats.linregress(df[x_ticker], df[y_ticker])
    regr_line = f'{y_ticker} = {regr.slope:.2f} {x_ticker} + {regr.intercept:.2f}'
    plt.figure(figsize=(7, 7))
    plt.plot(df[x_ticker], df[y_ticker], '.')
    plt.plot(df[x_ticker], regr.slope * df[x_ticker] + regr.intercept, 'r')
    plt.legend([f'{x_ticker} x {y_ticker}'], loc='best')
    plt.title(f'{x_ticker} x {y_ticker} (R = {regr.rvalue:.2f})')
    plt.xlabel(x_ticker)
    plt.ylabel(y_ticker)
    plt.show()

# 함수 호출 예제
linear_regression_analysis('MSFT', 'AAPL', '2000-01-04')
