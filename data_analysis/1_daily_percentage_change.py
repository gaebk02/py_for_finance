# 일간 변동률 daily percentage change
# 일간 변동률 = (당일 종가 - 전일 종가) / 전일 종가 * 100

import yfinance as yf
import matplotlib.pyplot as plt # 시각화 라이브러리

msft = yf.Ticker('MSFT').history() # 1년치 데이터 조회 / pandas.core.frame.DataFrame 객체를 반환

# 일간 변동률 계산
msft_dpc = ((msft['Close'] / msft['Close'].shift(1)) - 1) * 100 # 종가 사용 이유: 시장 참가자들의 최종적인 평가를 반영하며, 기술적 분석 및 차트에서의 중요성과 시장 외부 요인의 영향을 최소화
msft_dpc.iloc[0] = 0 # 첫 행은 비교 대상이 없으므로 0으로 설정
msft_dpc.head(5) # 상위 x행 조회

# 메소드화
def get_daily_percentage_change(ticker, start_date, end_date):
    history = yf.Ticker(ticker).history(start=start_date, end=end_date)
    dpc = ((history['Close'] / history['Close'].shift(1)) - 1) * 100
    dpc.iloc[0] = 0
    return dpc

# 히스토그램으로 도수분표 시각화

msft_dpc = get_daily_percentage_change('MSFT', '2024-01-01', '2024-12-31')
plt.hist(msft_dpc, bins=18) # 히스토그램 생성
plt.grid(True)
plt.show()

msft_dpc.describe() # 기술통계량(데이터를 요약) 확인 / count: 데이터 개수, mean: 평균, std: 표준편차, min: 최소값, 25%: 1사분위수, 50%: 중앙값, 75%: 3사분위수, max: 최대값
