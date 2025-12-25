import yfinance as yf
import pandas as pd
import numpy as np
def fetch_data(ticker_symbol,candleinterval,timeperiod):
    custom_names = ['Close','High','Low','Open','Volume','SMA_5','SMA_15','SMA_30']
    data = yf.download(ticker_symbol, interval=candleinterval, period=timeperiod)
    data['SMA_5'] = data['Close'].rolling(window=5,min_periods=2).mean()
    data['SMA_15'] = data['Close'].rolling(window=15,min_periods=2).mean()
    data['SMA_30'] = data['Close'].rolling(window=30,min_periods=2).mean()
    data.columns = custom_names
    try:
        data.index = data.index.tz_convert('Asia/Kolkata')
    except TypeError:
        data.index = data.index.tz_localize('UTC').tz_convert('Asia/Kolkata')
    data_newest_first = data.sort_index(ascending=False)
    return data_newest_first