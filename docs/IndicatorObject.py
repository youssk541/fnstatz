from LinksAndLists import Indices
import numpy as np
import yfinance as yf
import pandas as pd

class IndicatorObject:
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
        self.MA10 = None
        self.MA20 = None
        self.MA50 = None
        self.MA100 = None
        self.MA200 = None
        self.volume = None
        self.crossover10_20 = None
        self.crossover20_50 = None
        self.crossover50_200 = None
        self.open = None
        self.highLowSpread = None
        self.getStats()  # Initialisation

    def getStats(self):
        data = self.ticker.history("1y")
        try:
            self.tag = Indices[self.tag]
        except:
            pass
        self.dailyPctChange = np.log(data['Close'][-1] / data['Close'][-2]) * 100
        self.weeklyPctChange = np.log(data['Close'][-1] / data['Close'][-5]) * 100
        self.textToPublishDaily = " ".join([self.tag,
                                            'closed today at',
                                            str(data['Close'][-1]),
                                            '(',
                                            str("{0:.2f}".format(self.dailyPctChange)),
                                            '% daily change)'])
        self.high_52 = data['High'].max()
        self.low_52 = data['Low'].min()
        self.high_Month = data['High'][:-21].max()
        self.low_Month = data['Low'][:-21].min()
        self.MA10 = data['Close'].iloc[-10:].mean()
        self.MA20 = data['Close'].iloc[-20:].mean()
        self.MA50 = data['Close'].iloc[-50:].mean()
        self.MA100 = data['Close'].iloc[-100:].mean()
        self.MA200 = data['Close'].iloc[-200:].mean()
        self.crossover10_20 = 1 if self.MA10 < self.MA20 else -1
        self.crossover20_50 = 1 if self.MA20 < self.MA50 else -1
        self.crossover50_200 = 1 if self.MA50 < self.MA200 else -1
        self.volume = data['Volume'][-1]
        self.highLowSpread = data['High'][-1] - data['Low'][-1]

    def EndOfDayStats(self):  # For stocks
        return self.ticker.history(period="1d", interval='15m')['Close']

    def highFrequencyCheck(self):
        temp_data = self.ticker.history(period='1d', interval='15m')
        try:
            var = (temp_data['Close'][0] - temp_data['Open'][0]) / temp_data['Open'][0]
        except:
            return
        if abs(var * 100) >= 5:
            return [self.tag, round(var * 100, 3)]

    def checkForChange(self):
        message = ""
        high_52 = self.high_52
        low_52 = self.low_52
        high_Month = self.high_Month
        low_Month = self.low_Month
        crossover10_20 = self.crossover10_20
        crossover20_50 = self.crossover20_50
        crossover50_200 = self.crossover50_200

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

        if crossover10_20 * self.crossover10_20 == -1:
            upper = ["10", "20"] if crossover10_20 == 1 else ["20",
                                                              "10"]
            message += " ".join(["Moving average", upper[0], "days crosses over MA", upper[1], "for", self.tag, '\n'])

        if crossover20_50 * self.crossover20_50 == -1:
            upper = ["20", "50"] if crossover20_50 == 1 else ["50",
                                                              "20"]
            message += " ".join(["Moving average", upper[0], "days crosses over MA", upper[1], "for", self.tag, '\n'])

        if crossover50_200 * self.crossover50_200 == -1:
            upper = ["50", "100"] if crossover50_200 == 1 else ["100",
                                                          "50"]
            message += " ".join(["Moving average", upper[0], "days crosses over MA", upper[1], "for", self.tag,'\n'])

        return message


if __name__ == '__main__':
    pd.set_option("display.max_columns", 10)
    ticker = yf.Ticker("JPY=X")
    f=IndicatorObject("JPY=X")
