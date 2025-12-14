import yfinance as yf
import pandas as pd

def fetch_data(ticker_symbol,candleinterval,timeperiod):
    custom_names = ['Close','High','Low','Open','Volume']
    data = yf.download(ticker_symbol, interval=candleinterval, period=timeperiod)
    data.columns = custom_names
    try:
        data.index = data.index.tz_convert('Asia/Kolkata')
    except TypeError:
        data.index = data.index.tz_localize('UTC').tz_convert('Asia/Kolkata')
    data_newest_first = data.sort_index(ascending=False)
    return data_newest_first