import nse_data_fetcher as nse
import pandas_ta as ta
import numpy as np
import pandas as pd
import PreOpen as PO
import time
from Sendnotification import send_telegram_notification
from datetime import datetime

def getoneminutedata(ticker_symbol):
    data_1minute=nse.fetch_data(ticker_symbol+".NS","1m","5d")
    return  data_1minute


def get_signal_for_timeframe(df_1m, interval):
    resampled_df = df_1m.resample(interval).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }).dropna()
    resampled_df['SMA_5'] = resampled_df['Close'].rolling(window=5).mean()
    resampled_df['SMA_15'] = resampled_df['Close'].rolling(window=15).mean()
    if len(resampled_df) < 15:
        return "Insufficient Data"
    
    last_row = resampled_df.iloc[-1]
    prev_row = resampled_df.iloc[-2]
    if last_row['SMA_5'] > last_row['SMA_15']:
        return "Bullish"
    elif last_row['SMA_5'] < last_row['SMA_15']:
        return "Bearish"
    else:
        return "Neutral"
preopenstocks = PO.PreOpen()
#Run for all PreOpen Market Data Stocks to Every 30 mints
#Send Telegram Notification
for i in range(1):
    #time.sleep(1983)
    time.sleep(30)
    datafornotification = ""
    datafornotification = pd.DataFrame(columns=['Stock Symbol','Current 15-minute Trend','Current 30-minute Trend','Current 60-minute Trend'])
    for row in preopenstocks['symbol']:
        print("Ticker Value:"+row)
        data_1minute = getoneminutedata(row)
        signal_15m = get_signal_for_timeframe(data_1minute, '15T')
        signal_30m = get_signal_for_timeframe(data_1minute, '30T')
        signal_60m = get_signal_for_timeframe(data_1minute, '60T')
        datafornotification.loc[len(datafornotification)] = [row, signal_15m, signal_30m, signal_60m]
        time.sleep(0.5)
    markdown_msg = datafornotification.to_markdown(index=False)
    formatted_payload = f"```\n{markdown_msg}\n```"
    send_telegram_notification("Analysis report at Time:"+ datetime.now().strftime("%H:%M:%S") +"\n"+formatted_payload)
