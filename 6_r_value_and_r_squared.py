# 선형 회귀 분석 Linear Regression Analysis

# 상관계수 Correlation Coefficient, r-value
# 독립변수와 종속변수 사이의 관계를 나타내는 값, -1 ~ 1 사이의 값을 가짐
# 1: 완벽한 양의 상관관계, 리스크 완화효과가 없음
# 0: 상관관계가 없음, 높은 리스크 완화효과
# -1: 완벽한 음의 상관관계

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from spicy import stats # 선형 회귀 분석을 위한 라이브러리

kospi = yf.Ticker('^KS11').history(start='2000-01-04')
snp = yf.Ticker('^GSPC').history(start='2000-01-04')

snp.index = snp.index.tz_convert('Asia/Seoul') # 한국 시간으로 변경(x축인 미국으로 지정해도 되나, 한국 일자로 알기 쉽게 변경)
df = pd.DataFrame({'snp': snp['Close'], 'kospi': kospi['Close']})
df.index = df.index.normalize() # 날짜를 일자만 표시
df = df.groupby(df.index).mean() # 공통화
df = df.fillna(method='bfill') # 빈 값 채우기 backword fill, NaN 값을 뒤의 값으로 채움
df = df.fillna(method='ffill') # 빈 값 채우기 forward fill, NaN 값을 앞의 값으로 채움

# dataframe.corr() 함수를 통해 상관계수 확인
df.corr()
# 시리즈.corr() 함수를 통해 상관계수 확인
df['snp'].corr(df['kospi'])


# 결정계수 Coefficient of Determination, R-squared
# 상관계수의 제곱, 0 ~ 1 사이의 값을 가짐
# 예) r = 0.8 => r^2 = 0.64 => 64%의 설명력, 36%는 다른 요인에 의해 설명되는 것
# 상관관계가 아닌 회귀분석에서 사용하는 수치
r = df['snp'].corr(df['kospi'])
r_squared = r ** 2



regr = stats.linregress(df['snp'], df['kospi']) # 선형 회귀 분석
# LinregressResult(
# slope=0.432383342235192, # 기울기
# intercept=848.2818033445922, # y절편
# rvalue=0.7848509433426405, # r값(상관계수)
# pvalue=0.0, # p값
# stderr=0.004241622336829559, # 표준오차
# intercept_stderr=10.39271262291176) # y절편의 표준오차
