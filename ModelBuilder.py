import nse_data_fetcher as nse
import pandas_ta as ta
import numpy as np
import pandas as pd
ticker_symbol="HINDZINC"
data_1minute=nse.fetch_data(ticker_symbol+".NS","1m","2d")

file_name=ticker_symbol+".csv"
N=30
data_1minute.ta.rsi(append=True)
data_1minute['SMA_20'] = data_1minute['Close'].rolling(window=20,min_periods=1).mean()
data_1minute['SMA_9'] = data_1minute['Close'].rolling(window=9,min_periods=1).mean()
data_1minute['SMA_35'] = data_1minute['Close'].rolling(window=35,min_periods=1).mean()


#data_1minute['Above_Signal']=data_1minute['SMA_9']>data_1minute['SMA_20']
#data_1minute['Crossover_Detected'] = data_1minute['Above_Signal'] != data_1minute['Above_Signal'].shift(1)
#data_1minute['Direction'] = ['Bullish' if x else 'Bearish' for x in data_1minute['Above_Signal']]
#crossoverIndex = np.where(data_1minute['Crossover_Detected'] == True)[0]
data_1minute.to_csv(file_name)
#print(crossoverIndex)
#print(data_1minute)