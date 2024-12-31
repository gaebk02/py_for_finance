import yfinance as yf
import matplotlib.pyplot as plt

msft = yf.Ticker('MSFT') # 조회 주식 설정

msft.history() # 데이터 조회
# open: 시가, close: 종가, volume: 거래량, adj close: 수정 종가
msft.history(start="2024-01-01", end="2024-05-01") # 일정 지정
msft.history(period="1d") # 간격 지정 d / mo / y / max
msft.history().head(5) # 상위 x행 조회
msft.history()[['Open', 'Close']] # 원하는 항목만 조회



msft_history = yf.Ticker('MSFT').history() # 1년치 데이터 조회 / pandas.core.frame.DataFrame 객체를 반환
plt.plot(msft_history.index, msft_history.Close, 'b', label= "MS") #index 는 pandas.core.frame.DataFrame 객체의 속성 / Close는 객체의 열
# Open High Low Close Volume Dividends Stock Splits => 각 열
plt.plot(msft_history.index, msft_history.Close, 'r--', label= "MS with r")
plt.legend(loc='best')
plt.show()


# 주식 가격으로 주식을 비교하는 것은 어렵다. 비교를 위한 별개의 지표가 필요하다.

## 일간 변동률 daily percentage change
## 일간 변동률 = (당일 종가 - 전일 종가) / 전일 종가 * 100

msft_dpc = ((msft_history['Close'] / msft_history['Close'].shift(1)) - 1) * 100 # 일간 변동률 계산
msft_dpc.iloc[0] = 0 # 첫 행은 비교 대상이 없으므로 0으로 설정
msft_dpc.head(5) # 상위 x행 조회

# 히스토그램으로 도수분표 시각화
plt.hist(msft_dpc, bins=18) # 히스토그램 생성
plt.grid(True)
plt.show()

msft_dpc.describe() # 기술통계량(데이터를 요약) 확인 / count: 데이터 개수, mean: 평균, std: 표준편차, min: 최소값, 25%: 1사분위수, 50%: 중앙값, 75%: 3사분위수, max: 최대값


# 누적곱 cumulative product
# 일간변동률은 기하급수적 변화를 보이기 때문에 누적곱을 통해 전체적인 변동률을 확인한다.
# •	일간 변동률은 하루 동안의 자산(가격, 가치 등)이 얼마나 변했는지를 나타냅니다. 예를 들어, • 첫째 날: +2% 변동률은 1.02로 곱해져야 함. • 둘째 날: -1% 변동률은 0.99로 곱해져야 함. • 누적곱은 이 변동률을 차례대로 곱해 전체적인 변동을 반영합니다.
# •	누적곱은 이 변동률을 차례대로 곱해 전체적인 변동을 반영합니다. 예를 들어, • 첫째 날 이후: 1 \times 1.02 = 1.02 • 둘째 날 이후: 1.02 \times 0.99 = 1.0098 이는 2일 동안 약 0.98%의 증가를 나타냅니다. 단순히 변동률을 더한다면 1%의 증가로 잘못 계산됩니다.

msft_dpc_cp = ((100 + msft_dpc)/100).cumprod() * 100 - 100 # 누적곱 계산


def get_cumulative_product(ticker, start_date, end_date):
    history = yf.Ticker(ticker).history(start=start_date, end=end_date)
    dpc = ((history['Close'] / history['Close'].shift(1)) - 1) * 100
    dpc.iloc[0] = 0
    dpc_cp = ((100 + dpc) / 100).cumprod() * 100 - 100
    return dpc_cp

msft_dpc_cp = get_cumulative_product('MSFT', '2024-01-01', '2024-12-31')
aapl_dpc_cp = get_cumulative_product('AAPL', '2024-01-01', '2024-12-31')

plt.plot(msft_dpc_cp.index, msft_dpc_cp, 'b', label='MSFT')
plt.plot(aapl_dpc_cp.index, aapl_dpc_cp, 'r', label='AAPL')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()


# 최대 손실 낙폭 Maximum Drawdown
# 최고점에서 최저점까지의 가장 큰 손실 / 손실을 취소화하는 퀀트 투자에서는 mdd를 가장 중요시 하는 것이 좋다고도 한다.

# S&P500 지수의 MDD

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


## 지수화 Indexation
## 누적곱과 지수화의 차이점
## 누적곱은 실질적인 수익률을 확인, 지수화는 여러 자산의 상대적인 성과를 비교.
## 주가를 100으로 지수화하여 비교하는 방법


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


## 산점도 Scatter Plot
## 독립변수 x와 종속변수 y 사이의 관계를 나타내는 그래프
## 가로축은 독립변수 x, 세로축은 종속변수 y
## 미국시장과 한국시장의 상관관계를 산점도로 확인, snp는 x축, kospi는 y축
## 점의 분포가 y = x인 직선 형태가 될 수록 직접적인 관계가 있음, 산점도만으로는 정확한 분석이 어려우므로 선형 회귀 분석을 통해 확인

import pandas as pd
len(snp), len(kospi) # 데이터 길이 확인 / 개장일이 다르다보니, 두 길이가 다름
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


## 선형 회귀 분석 Linear Regression Analysis
from spicy import stats # 선형 회귀 분석을 위한 라이브러리
regr = stats.linregress(df['snp'], df['kospi']) # 선형 회귀 분석
# LinregressResult(
# slope=0.432383342235192, # 기울기
# intercept=848.2818033445922, # y절편
# rvalue=0.7848509433426405, # r값(상관계수)
# pvalue=0.0, # p값
# stderr=0.004241622336829559, # 표준오차
# intercept_stderr=10.39271262291176) # y절편의 표준오차


# 상관계수 Correlation Coefficient, r-value
# 독립변수와 종속변수 사이의 관계를 나타내는 값, -1 ~ 1 사이의 값을 가짐
# 1: 완벽한 양의 상관관계, 리스크 완화효과가 없음
# 0: 상관관계가 없음, 높은 리스크 완화효과
# -1: 완벽한 음의 상관관계

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



# S&P500과 KOSPI의 선형 회귀 분석 결과를 산점도와 함께 시각화
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
