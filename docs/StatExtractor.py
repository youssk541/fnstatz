from .LinksAndLists import Indices
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class indicatorObject:
    def __init__(self, tag):
        self.tag = tag
        self.ticker = yf.Ticker(self.tag)
        self.open = None
        self.dailyPctChange = None
        self.weeklyPctChange = None
        self.textToPublishDaily = None
        self.textToPublishWeekly = None
        self.high_52 = None
        self.low_52 = None
        self.high_Month = None
        self.low_Month = None
        self.MA50 = None
        self.MA100 = None
        self.MA200 = None
        self.volume=None
        self.crossover = None
        self.open = None
        self.highLowSpread = None
        self.getStats() #Initialisation

    # def getDailyChange(self):  # FAIRE ATTENTION AU MOMENT D EXECUTION , PEUT CAUSER OOB EXCEPTION
    #     data = self.ticker.history("2d")
    #     pctChange = np.log(data['Close'][1] / data['Close'][0]) * 100
    #     textToPublish = " ".join(['Le', Indices[self.tag], 'cloture à', str(data['Close'][1]), '(',
    #                               str("{0:.2f}".format(pctChange)), '% daily change)'])
    #     return [pctChange, data['Close'][1], data['High'][1], data['Low'][1], textToPublish]

    def getStats(self):
        data = self.ticker.history("1y")
        try :
            self.tag=Indices[self.tag]
        except:
            pass
        self.dailyPctChange = np.log(data['Close'][-1] / data['Close'][-2]) * 100
        self.weeklyPctChange= np.log(data['Close'][-1] / data['Close'][-5]) * 100
        self.textToPublishDaily = " ".join(['Le',self.tag,
                                       'cloture à',
                                       str(data['Close'][-1]),
                                       '(',
                                       str("{0:.2f}".format(self.dailyPctChange)),
                                       '% variation journalière)']) # On le garde comme attribut car il utilise data (donc non accessible depuis une méthode extérieure)
        self.textToPublishWeekly = " ".join(['Le',self.tag,
                                       'cloture à',
                                       str(data['Close'][-1]),
                                       '(',
                                       str("{0:.2f}".format(self.weeklyPctChange)),
                                       '% variation journalière)'])

        self.high_52 = data['High'].max()
        self.low_52 = data['Low'].min()
        self.high_Month = data['High'][:-21].max()
        self.low_Month = data['Low'][:-21].min()
        self.MA50 = data['Close'].iloc[-50:].mean()
        self.MA100 = data['Close'].iloc[-100:].mean()
        self.MA200 = data['Close'].iloc[-200:].mean()
        self.crossover1 = 1 if self.MA50 < self.MA200 else -1
        self.volume= data['Volume'][-1]
        self.highLowSpread = data['High'][-1]-data['Low'][-1]

    def EndOfDayStats(self): # For stocks
        return self.ticker.history(period="1d",interval='15m')['Close']


    def refreshWeekly(self):
        self.getstats()

    def highFrequencyCheck(self):
        tempData=self.ticker.history(period='1d', interval='15m')
        try:
            var = (tempData['Close'][0]-tempData['Open'][0])/tempData['Open'][0]
        except:
            return
        if (abs(var*100)>=5):
            return [self.tag , round(var * 100, 3)]

    def checkForChange(self):
        message = ""
        ##### Attributs au temps N-1
        high_52 = self.high_52
        low_52 = self.low_52
        high_Month = self.high_Month
        low_Month = self.low_Month
        crossover = self.crossover
        self.getStats()
        if self.low_Month < low_Month:
            if self.low_52 < low_52:
                message += "New Low in 52 weeks for " + self.tag + " at " + str(self.low_52) + '\n'
            else:
                message += "New Low in a month for " + self.tag + " at " + str(self.low_Month) + '\n'
        if self.high_Month > high_Month:
            if self.high_52 > high_52:
                message += "New high in 52 weeks for " + self.tag + " at " + str(self.high_52) + '\n'
            else:
                message += "New high in a month for " + self.tag + " at " + str(self.high_Month) + '\n'

        if crossover * self.crossover == -1:
            upper = ["50", "100"] if crossover == 1 else ["100","50"]  # Si on passe de 1 à -1 MA50 > MA100 , et vice versa
            message += " ".join(["Moving average", upper[0], "days crosses over MA", upper[1], "for", self.tag])
        return message



if __name__ == '__main__':
    pd.set_option("display.max_columns",10)
    ticker = yf.Ticker("AAPL")
    tempData = ticker.history(period="1d",interval='1m')
    print(tempData)
    tempData['Close'].plot.box()
    plt.show()
