# 누적곱 cumulative product
# 일간변동률은 기하급수적 변화를 보이기 때문에 누적곱을 통해 전체적인 변동률을 확인한다.
# •	일간 변동률은 하루 동안의 자산(가격, 가치 등)이 얼마나 변했는지를 나타냅니다. 예를 들어, • 첫째 날: +2% 변동률은 1.02로 곱해져야 함. • 둘째 날: -1% 변동률은 0.99로 곱해져야 함. • 누적곱은 이 변동률을 차례대로 곱해 전체적인 변동을 반영합니다.
# •	누적곱은 이 변동률을 차례대로 곱해 전체적인 변동을 반영합니다. 예를 들어, • 첫째 날 이후: 1 \times 1.02 = 1.02 • 둘째 날 이후: 1.02 \times 0.99 = 1.0098 이는 2일 동안 약 0.98%의 증가를 나타냅니다. 단순히 변동률을 더한다면 1%의 증가로 잘못 계산됩니다.

import yfinance as yf
import matplotlib.pyplot as plt

msft = yf.Ticker('MSFT').history()

# 일간 변동률 계산
msft_dpc = ((msft['Close'] / msft['Close'].shift(1)) - 1) * 100
msft_dpc.iloc[0] = 0

# 누적곱 계산
msft_dpc_cp = ((100 + msft_dpc) / 100).cumprod() * 100 - 100

# 메소드화
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

