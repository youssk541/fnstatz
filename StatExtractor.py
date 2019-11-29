import pandas_datareader.data as web
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import yahoo_finance as yf
import yfinance as fyf
fyf.pdr_override()
class indicatorObject():
    def __init__(self, tag):
        self.tag = tag
        self.getMovingAverage()
        self.getHighLow()


    def getDailyChange(self): # FAIRE ATTENTION AU MOMENT D EXECUTION , PEUT CAUSER OOB EXCEPTION
        start = datetime.strftime(datetime.today() - timedelta(days=80), '%Y-%m-%d')
        end = datetime.strftime(datetime.today(), '%Y-%m-%d')
        data = web.DataReader(self.tag,'yahoo' ,start=start, end=end)
        #pctChangement = np.log(data['Close'][1] / data['Close'][0]) * 100
        return data


    def getMovingAverage(self):
        start = datetime.strftime(datetime.today() - timedelta(days=200), '%Y-%m-%d')
        end = datetime.strftime(datetime.today(), '%Y-%m-%d')
        data = web.get_data_yahoo(self.tag,  start=start, end=end)
        self.MA50=data['Close'].iloc[-(50-2*50//7):]
        self.MA100=data['Close'].mean()

    def getHighLow(self):
        start = datetime.strftime(datetime.today() - timedelta(days=365), '%Y-%m-%d')
        end = datetime.strftime(datetime.today(), '%Y-%m-%d')
        data = web.get_data_yahoo(self.tag, start=start, end=end)
        self.high_52 = data['Close'].max()
        self.low_52 = data['Close'].min()



###                     EUROBANK                        ###
EuroBankIndexx = indicatorObject("EGFEY")

###                      GOLD                           ###
GC = indicatorObject("GC=F")
ARCA = indicatorObject("^HUI")

###                     SILVER                          ###
a = indicatorObject("^XAU")
###     OIL         ###
wti = indicatorObject("WTI")  # USED IN US MARKETS
brent = indicatorObject("BZ=F")  # EXTRACTED IN THE NORTH SEA
### I would liek to add dubai oil

###             EXCHANGE INDEX : GLOBAL                    ###
SP100 = indicatorObject("^OOI")
SP100 = indicatorObject("^SPG1200")
GDOW = indicatorObject("^GDOW")

###             EXCHANGE INDEX : AMERIQUE DU NORD          ###
DJI = indicatorObject("^DJI")
SP500 = indicatorObject("^GSPC")
NASDAQ = indicatorObject("^IXIC")

###             EXCHANGE INDEX : EUROPE (local)          ###
DAX = indicatorObject("^GDAXI")
CAC40 = indicatorObject("^FCHI")
FTSE = indicatorObject("^FTSE")

###             EXCHANGE INDEX : EUROPE (global)          ###
Stoxx50 = indicatorObject("^STOXX50E")
Stoxx600 = indicatorObject("^STOXX")

###             EXCHANGE INDEX : ASIA 50
AsiaSP50=indicatorObject('V2TX')
###             VOLATILITY                              ###
Vol_SP500=indicatorObject("^VIX")

# def getinfo(source):
#     data = pdmx.Request(source)
#     DSD = data.dataflow()
#     with pd.option_context('display.max_rows', None):
#         print(DSD.dataflow)
#
# def getinfo(source, table):
#     data = pdmx.Request(source)
#     DSD = data.dataflow(table)
#     with pd.option_context('display.max_rows', None):
#         print(DSD.write())

if __name__ == "__main__":
    DAX.getHighLow()
    print(DAX.low_52)