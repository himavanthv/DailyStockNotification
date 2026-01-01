from nsepython import nse_preopen
from nsepython import nse_preopen_movers
from datetime import datetime
import pandas as pd
from nsepython import nse_get_top_gainers, nse_get_top_losers
from Sendnotification import send_telegram_notification

def PreOpen():
    nifty_preopen_data = nse_preopen(key="ALL", type="pandas")
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d%b%Y")
    stockstoberetained = pd.read_csv('AllOptionsStocks.csv')
    stocklist = stockstoberetained['Symbol']
    mask = nifty_preopen_data['symbol'].isin(stocklist)
    stockstobeconsidered=nifty_preopen_data[mask]
    morethan1pcchange = abs(stockstobeconsidered['pChange']) > 1
    finalobservationstocks = stockstobeconsidered[morethan1pcchange]
    return finalobservationstocks

def get_top_gainers():
    gainers = nse_get_top_gainers()
    return gainers

def get_top_losers():
    losers = nse_get_top_losers()
    return losers


