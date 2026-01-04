import nse_data_fetcher as nse
import numpy as np
import pandas as pd
import time
import pytz
from Sendnotification import send_telegram_notification
from datetime import datetime

def getoneminutedata(ticker_symbol):
    data=nse.fetch_data(ticker_symbol+".NS","15m","15d")
    return  data


def performanalysis(data):
    data.dropna(inplace=True)
    dataLen=len(data)
    prev_short = data['SMA_9'].iloc[1]
    prev_long = data['SMA_26'].iloc[1]
    curr_short = data['SMA_9'].iloc[0]
    curr_long = data['SMA_26'].iloc[0]
    latestshort = data['SMA_9'].iloc[0]
    latestlong = data['SMA_26'].iloc[0]
    currropen=data['Open'].iloc[0]
    prevclose=data['Close'].iloc[1]
    prevopen=data['Open'].iloc[1]
    currrsi=data['RSI_14'].iloc[0]
    prevrsi1=data['RSI_14'].iloc[1]
    prevrsi2=data['RSI_14'].iloc[2]
    prevrsi3=data['RSI_14'].iloc[3]
    prevchange = ((prevclose-prevopen)/prevopen)*100
    percentma=((latestshort-latestlong)/latestshort)*100
    if prev_short <= prev_long and curr_short > curr_long and currropen>curr_short and currrsi>prevrsi1 and prevrsi1>prevrsi2 and prevrsi2>prevrsi3 and currrsi>60:
        return "BULLISH Crossover detected on the current (most recent closed) candle."
    elif prev_short >= prev_long and curr_short < curr_long and currropen<curr_short and currrsi<prevrsi1 and prevrsi1<prevrsi2 and prevrsi2<prevrsi3 and currrsi<40:
        return "BEARISH Crossover detected on the current (most recent closed) candle."
    else:
        return "No new crossover detected on the latest candle."

ist_timezone = pytz.timezone('Asia/Kolkata')
allstocks = pd.read_csv('AllOptionsStocks.csv')

for i in range(1):
    #print('Start Time '+datetime.now(ist_timezone).strftime("%H:%M:%S"))
    datafornotification = ""
    datafornotification = pd.DataFrame(columns=['Stock Symbol','Analysis'])
    for index, row in allstocks.iterrows():
        symbol = row['Symbol']
        try:
            data_1minute = getoneminutedata(symbol)
        except:
            print('Download Error '+ symbol)
            continue
        analysisresult = performanalysis(data_1minute)
        if analysisresult=='No new crossover detected on the latest candle.':
            continue
        datafornotification.loc[len(datafornotification)] = [symbol,analysisresult]
    markdown_msg = datafornotification.to_markdown(index=False)
    formatted_payload = f"```\n{markdown_msg}\n```"
    current_time_ist = datetime.now(ist_timezone)
    print('End Time '+datetime.now(ist_timezone).strftime("%H:%M:%S"))
    #print(datafornotification)
    send_telegram_notification("Analysis report at Time:"+ current_time_ist.strftime("%H:%M:%S") +"\n"+formatted_payload)