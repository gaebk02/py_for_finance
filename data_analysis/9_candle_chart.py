# 캔들 차트 Candle Chart

import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
import mplfinance as mpf

msft = yf.Ticker('MSFT').history(start='2024-11-01')
kwargs = dict(type='candle', volume=True, title='MSFT Candle Chart', mav=(12)) #mav란 Moving Average의 약자로 이동평균선을 그리는 옵션
mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(msft, **kwargs, style=s)
