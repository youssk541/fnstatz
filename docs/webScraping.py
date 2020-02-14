from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from .LinksAndLists import url_dict_inflation, month_swap_dict
from datetime import datetime
from .tweepy_streamer import TwitterClient
import pandas as pd
import numpy as np


def scrape(url):
    uClient = uReq(url)
    page = uClient.read()
    import codecs
    page_soup_html = soup(codecs.decode(page, 'utf-8'), "html.parser")
    data = page_soup_html.findAll("tr", {"class": ["tabledata1", "tabledata2"]})
    return data


def frenchDateToDatetime(str):
    str = str.split(sep=" ")
    if (len(str)==3): # Day Month Year
        str[0], str[1] = str[1], str[0]
        str[0] = month_swap_dict[str[0]]
        return datetime.strptime(str[0] + " " + str[1] + " " + str[2], '%b %d %Y')
    else:
        str[0] = month_swap_dict[str[0].strip('%\xa0')]
        return datetime.strptime(str[0]+" " + str[1], '%b %Y')


class inflation_Container():
    def __init__(self,urlIndex):
        self.tag = urlIndex
        self.url = url_dict_inflation[urlIndex]
        self.data = scrape(self.url)
        self.Monthly = self.getMonthly()
        self.Yearly = self.getYearly()
        self.data=None

    def getMonthly(self):
        df_monthly = pd.DataFrame(columns=['Taux'])
        for i in range(10):
            element = self.data[i].findAll('td')
            df_monthly.loc[frenchDateToDatetime(element[0].text)] = [float(element[1].text.strip('%\xa0').replace(',','.'))]
        return df_monthly

    def getYearly(self):
        df_yearly = pd.DataFrame(columns=['Taux'])
        for i in range(10, 20):
            element = self.data[i].findAll('td')
            df_yearly.loc[frenchDateToDatetime(element[0].text)] = [float(element[1].text.strip('%\xa0').replace(',','.'))]
        return df_yearly

    def refresh(self):
        self.data=scrape(self.url)
        self.getMonthly()
        self.getYearly()
        self.data=None
# class rate_Container():
#
#     def __init__(self, urlIndex):
#         self.tag = urlIndex
#         self.url = url_dict[urlIndex]
#         self.data = scrape(self.url)
#         self.Daily = self.getDaily()
#         self.Monthly = self.getMonthly()
#         self.Yearly = self.getYearly()
#         self.data = None
#
#     def getDaily(self):
#         df_daily = pd.DataFrame(columns=['Date', 'Taux'])
#         for i in range(12):
#             element = self.data[i].findAll('td')
#             df_daily.loc[i] = [frenchDateToDatetime(element[0].text), float(element[1].text.strip('%\xa0').replace(',','.'))]
#         return df_daily
#
#     def getMonthly(self):
#         df_monthly = pd.DataFrame(columns=['Date', 'Taux'])
#         for i in range(12, 24):
#             element = self.data[i].findAll('td')
#             df_monthly.loc[i % 12] = [frenchDateToDatetime(element[0].text), float(element[1].text.strip('%\xa0').replace(',','.'))]
#         return df_monthly
#
#     def getYearly(self):
#         df_yearly = pd.DataFrame(columns=['Date', 'Taux'])
#         for i in range(24, 36):
#             element = self.data[i].findAll('td')
#             df_yearly.loc[i % 24] = [frenchDateToDatetime(element[0].text), float(element[1].text.strip('% ').replace(',','.'))]
#         return df_yearly
#
#     def updateDaily(self):
#         pass

class governmentRateContainer():
    def __init__(self):
        self.url = "https://fr.global-rates.com/taux-de-interets/banques-centrales/banque-centrale-europeenne/taux-de-bce.aspx"
        self.data=self.governmentRates()

    def governmentRates(self):
        data = scrape(self.url)
        govRates = pd.DataFrame(columns=['Titre', 'Taux', 'Date changement'])
        for i in range(10, 20):
            infos = data[i].find_all('td')
            govRates.loc[i - 10] = (infos[0].text, infos[2].text, infos[3].text)
        return govRates

    def checkGovernmentRateChange(self):
        data = self.governmentRates()
        truth = np.where(data['Date changement'] == self.data['Date changement'])[0]
        if len(truth) > 0:
            message = ""
            for i in truth:
                m = data.loc[i]
                message += " ".join(["Nouveau taux", m['Titre'], m['Taux']]) + '\n'
            self.data=data
            publisher = TwitterClient()
            publisher.publish_tweet(message)

# def getVstoxx():
#     url = 'https://www.stoxx.com/index-details?symbol=V2TX'
#     page = uReq(url).read()
#     page_soup_html = soup(page, 'html5lib')
#     container = page_soup_html.find('tr', {'class': 'last'})
#     print(container)
#     print(container.find('td', {'id': "overview-last-value"}))

# for i in range(500):
#     tickers.append(yf.Ticker(listSP500[i]))
#     tickers[i].history(period='1d')