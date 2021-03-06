import concurrent.futures
import pickle
import re
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.request import urlopen as uReq
import matplotlib.pyplot as plt
import requests
from pandas.plotting import table
from bs4 import BeautifulSoup as soup

from webScraping import *
from IndicatorObject import IndicatorObject

import yfinance as yf
"""
        USEFUL FUNCTIONS
"""


def pickleObjectList(objectList, fileName):
    with open(fileName, "wb") as f:
        pickle.dump(len(objectList), f)
        for value in objectList:
            pickle.dump(value, f)


def getBreadth(stock_object_list):
    advances, declines, volumeAdvances, volumeDeclines = 0, 0, 0, 0
    for stock in stock_object_list:
        if stock.dailyPctChange > 0:
            advances += 1
            volumeAdvances += stock.volume
            continue
        declines += 1
        volumeDeclines += stock.volume
    return [int(advances), int(declines), int(volumeAdvances), int(volumeDeclines)]


""" 

        INTRADAY UPDATES        

"""


def highFrequencyUpdateEuropeanStocks(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return

    if not "09:15:00" < datetime.strftime(datetime.now(), "%X") < "18:15:00":  # Open times including GB/France/Germany
        return

    stockIndicatorObjects = []
    message = ""
    with open(pickledDataDirectoryPath + "/CAC40.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/DAX.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/FTSE.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.highFrequencyCheck, stockIndicatorObjects)):
            try:
                increaseType = "⬆" if response[1] > 0 else "🔻"
                message += " ".join([response[0], ":", str(response[1]), "%", increaseType, '\n'])
            except:
                pass
    if message:
        try:
            publisher.publish_tweet("Euro market in the last 15 minutes:" + '\n' + message)
        except:
            pass

def highFrequencyUpdateAmericanStocks(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    if not "15:45:00" <= datetime.strftime(datetime.now(), "%X") < "22:15:00":  # Open times for US markets
        return
    stockIndicatorObjects = []
    message = ""
    with open(pickledDataDirectoryPath + "/SP500.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.highFrequencyCheck, stockIndicatorObjects)):
            try:
                increaseType = "⬆" if response[1] > 0 else "🔻"
                message += " ".join([response[0], ":", str(response[1]), "%", increaseType, '\n'])
            except:
                pass
    if message:
        publisher.publish_tweet("US market in the last 15 minutes:" + '\n' + message)

""" 

        DAILY UPDATES        

"""


def dailyUpdateEuropean(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    IndicesIndicatorObjects = []
    with open(pickledDataDirectoryPath + "/Indices.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            IndicesIndicatorObjects.append(pickle.load(f))
    message = ""
    for i in range(3, 7):
        IndicesIndicatorObjects[i].checkForChange()
        message += IndicesIndicatorObjects[i].textToPublishDaily + '\n'
    publisher.publish_tweet(message)


def dailyUpdateCommodities(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    IndicesIndicatorObjects = []
    with open(pickledDataDirectoryPath + "/Indices.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            IndicesIndicatorObjects.append(pickle.load(f))
    message = ""
    for i in range(7, len(Indices)):
        IndicesIndicatorObjects[i].checkForChange()
        message += IndicesIndicatorObjects[i].textToPublishDaily + '\n'
    publisher.publish_tweet(message)


def dailyUpdateAmerican(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    # if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
    #     return
    IndicesIndicatorObjects = []
    with open(pickledDataDirectoryPath + "/Indices.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            IndicesIndicatorObjects.append(pickle.load(f))
    message = ""
    for i in range(0, 3):
        IndicesIndicatorObjects[i].checkForChange()
        message += IndicesIndicatorObjects[i].textToPublishDaily + '\n'
    publisher.publish_tweet(message)


def endOfDayEuropeanStockMarket(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    stockIndicatorObjects = []
    top10spreads = pd.DataFrame(columns=['highLowSpread'])

    with open(pickledDataDirectoryPath + "/CAC40.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/DAX.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/FTSE.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:  # Rafraichit les données de la base et récupère les spreads high low
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.getStats, stockIndicatorObjects)):
            top10spreads.loc[indicator] = indicator.highLowSpread

    pickleObjectList(stockIndicatorObjects[:40], pickledDataDirectoryPath + "/CAC40.dat")
    pickleObjectList(stockIndicatorObjects[40:70], pickledDataDirectoryPath + "/DAX.dat")
    pickleObjectList(stockIndicatorObjects[70:], pickledDataDirectoryPath + "/FTSE.dat")

    breadthDf = pd.DataFrame(columns=['Advances ⬆️' , 'Declines ⬇️','Volume ⬆️ ', 'Volume ⬇️'])
    breadthDf.loc['CAC40'] = getBreadth(stockIndicatorObjects[:40])
    breadthDf.loc['FTSE'] = getBreadth(stockIndicatorObjects[70:])
    breadthDf.loc['DAX'] = getBreadth(stockIndicatorObjects[40:70])


    top10spreads = top10spreads.sort_values('highLowSpread', ascending=False).head(10).index
    top10spreadsData = pd.DataFrame()
    fig, axs = plt.subplots(2, 5)
    for i in range(10):
        top10spreadsData[top10spreads[i].tag] = top10spreads[i].EndOfDayStats()
        time.sleep(0.01)
    for i in range(10):
        axs[i // 5, i % 5].boxplot(top10spreadsData[top10spreads[i].tag])
        axs[i // 5, i % 5].set_title(top10spreads[i].tag)
        axs[i // 5, i % 5].axes.get_xaxis().set_ticks([])
        axs[i // 5, i % 5].tick_params(axis='y', labelsize=7)
        time.sleep(0.01)

    fig.subplots_adjust(hspace=0.5, wspace=1.5)
    plt.savefig(repositoryDirectory + '/EODeuroMarket' + str(datetime.today().date()) + '.png', dpi=199)

    plt.clf()

    fig, axs = plt.subplots(2,1)  # no visible frame
    axs[0].patch.set_visible(False)
    axs[1].patch.set_visible(False)

    axs[0].axis('off')
    axs[1].axis('off')

    table(ax=axs[0], data=breadthDf)
    plt.savefig(repositoryDirectory +"/EUbreadth"+str(datetime.today().date()) +'.png')

    publisher.tweet_image("EUROPE: Top 10 movements in blue-chip stock market / Advance - Decline",
                          [repositoryDirectory + '/EODeuroMarket' + str(datetime.today().date()) + '.png',
                           repositoryDirectory + "/EUbreadth" + str(datetime.today().date()) + '.png']
                          )


def endOfDayUsStockMarket(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return

    stockIndicatorObjects = []
    top10spreads = pd.DataFrame(columns=['highLowSpread'])

    with open(pickledDataDirectoryPath + "/SP500.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:  # Rafraichit les données de la base et récupère les spreads high low
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.getStats, stockIndicatorObjects)):
            top10spreads.loc[indicator] = indicator.highLowSpread

    with concurrent.futures.ProcessPoolExecutor() as executor:  # Rafraichit les données de la base et récupère les spreads high low
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.checkForChange, stockIndicatorObjects)):
            top10spreads.loc[indicator] = indicator.highLowSpread

    pickleObjectList(stockIndicatorObjects, pickledDataDirectoryPath + "/SP500.dat")

    breadthDf = pd.DataFrame(columns=['Advances ⬆️', 'Declines ⬇️', 'Volume ⬆️ ', 'Volume ⬇️'])
    breadthDf.loc['SP500'] = getBreadth(stockIndicatorObjects)

    top10spreads = top10spreads.sort_values('highLowSpread', ascending=False).head(10).index
    top10spreadsData = pd.DataFrame()
    fig, axs = plt.subplots(2, 5)
    for i in range(10):
        top10spreadsData[top10spreads[i].tag] = top10spreads[i].EndOfDayStats()
        time.sleep(0.01)
    for i in range(10):
        axs[i // 5, i % 5].boxplot(top10spreadsData[top10spreads[i].tag])
        axs[i // 5, i % 5].set_title(top10spreads[i].tag)
        axs[i // 5, i % 5].axes.get_xaxis().set_ticks([])
        axs[i // 5, i % 5].tick_params(axis='y', labelsize=7)
        time.sleep(0.01)

    fig.subplots_adjust(hspace=0.5, wspace=1.5)

    plt.savefig(repositoryDirectory + '/EODUSMarket' + str(datetime.today().date()) + '.png', dpi=199)

    plt.clf()

    fig, axs = plt.subplots(2, 1)  # no visible frame
    axs[0].patch.set_visible(False)
    axs[1].patch.set_visible(False)

    axs[0].axis('off')
    axs[1].axis('off')

    table(ax=axs[0], data=breadthDf)
    plt.savefig(repositoryDirectory + "/USbreadth" + str(datetime.today().date()) + '.png')

    publisher.tweet_image("US : Top 10 movements in blue-chip stock market / Advance - Decline",
                          [repositoryDirectory + '/EODUSMarket' + str(datetime.today().date()) + '.png',
                           repositoryDirectory + "/USbreadth" + str(datetime.today().date()) + '.png']
                          )


def checkForChangesEUR(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    stockIndicatorObjects = []
    top10spreads = pd.DataFrame(columns=['highLowSpread'])
    message=""
    with open(pickledDataDirectoryPath + "/CAC40.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/DAX.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with open(pickledDataDirectoryPath + "/FTSE.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.checkForChange, stockIndicatorObjects)):
            if response:
                publisher.publish_tweet(response)


def checkForChangesUS(publisher):
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    stockIndicatorObjects = []
    message = ""

    with open(pickledDataDirectoryPath + "/SP500.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            stockIndicatorObjects.append(pickle.load(f))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for indicator, response in zip(stockIndicatorObjects,
                                       executor.map(IndicatorObject.checkForChange, stockIndicatorObjects)):
            if response:
                publisher.publish_tweet(response)


def updateEuropeanRateFile():
    if not datetime.today().weekday() <= 5:  # If it's not a weekday, no update
        return
    link = 'https://sdw-wsrest.ecb.europa.eu/service/data/YC/B.U2.EUR.4F.G_N_A+G_N_C.SV_C_YM.?lastNObservations=1'
    byteData = requests.get(link).content.splitlines(keepends=True)
    byteData = [b'<?xml version="1.0" encoding="UTF-8"?>'] + byteData[12:-1]
    byteData = b''.join(byteData)
    byteData = re.sub(b'generic:', b'', re.sub(b'message:', b'', byteData))
    f = tempfile.TemporaryFile()
    f.write(byteData)
    f.seek(0)
    tree = ET.parse(f)
    Spot_Rates = pd.DataFrame(columns=Maturities_Spot_Rate)
    Instant_Forward_Rates = pd.DataFrame(columns=Maturities_Instant_Forward)

    for period in Maturities_Spot_Rate:
        for element in (tree.findall("./Series/SeriesKey/Value[@value='" + period + "']/../../Obs")):
            date = element.find('./ObsDimension').attrib['value']
            value = float(element.find('./ObsValue').attrib['value'])
            Spot_Rates.at[date, period] = value

    for period in Maturities_Instant_Forward:
        for element in (tree.findall("./Series/SeriesKey/Value[@value='" + period + "']/../../Obs")):
            date = element.find('./ObsDimension').attrib['value']
            value = float(element.find('./ObsValue').attrib['value'])
            Instant_Forward_Rates.at[date, period] = value

    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        Spot_Rates.to_csv(rateFileDirectory + '/Spot_Rates.csv', sep='\t', mode='a', header=None)
        Instant_Forward_Rates.to_csv(rateFileDirectory + '/Instant_Forward_Rates.csv', sep='\t', mode='a', header=None)

    return Spot_Rates.T, Instant_Forward_Rates.T  # Transposés pour pouvoir être plotés


def updateUSRateFile():
    if not datetime.today().weekday() <= 5:  # If it's not a weekday, no update
        return
    link = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=2020'

    def floatify(string):
        try:
            return float(string)
        except:
            return 'N/A'

    uClient = uReq(link)
    page = uClient.read()
    import codecs
    page_soup_html = soup(codecs.decode(page, 'utf-8'), "html.parser")
    data = page_soup_html.find("table", {"class": ["t-chart"]}).findAll('tr')
    treasury_yields = pd.DataFrame(columns=[string.text for string in data[0].findAll('th')[1:]])

    for element in data:
        row = element.findAll('td')
        if (row):
            treasury_yields.loc[datetime.strptime(row[0].text, "%m/%d/%y")] = [floatify(element.text) for element in
                                                                               row[1:]]
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        treasury_yields.to_csv(rateFileDirectory + '/treasuryTest.csv', sep='\t', mode='a', header=None)
    return treasury_yields.T[-1]


def rateUpdate():  # Only use is to schedule them both at the same time
    if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
        return
    updateEuropeanRateFile()
    updateUSRateFile()


"""

        WEEKLY UPDATES
        
"""


def YieldCurve(publisher):
    US_X_axis = [0.08333333, 0.16666667, 0.25, 0.5, 1.,
                 2., 3., 5., 7., 10.,
                 20., 30.]
    EU_X_axis = [0.25, 0.5, 0.75, 1., 2., 3., 4., 5., 6.,
                 7., 8., 9., 10., 11., 12., 13., 14., 15.,
                 16., 17., 18., 19., 20., 21., 22., 23., 24.,
                 25., 26., 27., 28., 29., 30.]
    Spot_Rates, Instant_Forward_Rates = updateEuropeanRateFile()  # Deja transposées ici
    US_spot_rate = updateUSRateFile()
    Spot_Rates['X_axis'] = EU_X_axis
    Instant_Forward_Rates['X_axis'] = EU_X_axis
    US_spot_rate['X_axis'] = US_X_axis
    plt.plot(Spot_Rates['X_axis'], Spot_Rates.iloc[:, 0], label='Spot rate Euro area', marker='+')
    plt.plot(Instant_Forward_Rates['X_axis'], Instant_Forward_Rates.iloc[:, 0], label='Instant Forward Euro are',
             marker='+')
    plt.plot(US_spot_rate['X_axis'], US_spot_rate.iloc[:, 0], label='US Spot treasury yield ', marker='+')
    plt.xlabel('Years')
    plt.ylabel('Rate(%)')
    plt.legend(loc=4, prop={'size': 7})
    plt.savefig(repositoryDirectory + '/Yield_' + Spot_Rates.keys()[0] + '.png', dpi=199)
    publisher.tweet_image("Yield curve : " + str((datetime.today() - timedelta(days=1)).strftime('%d %b %Y')),
                          repositoryDirectory + '/Yield_' + Spot_Rates.keys()[0] + '.png')
    return repositoryDirectory + 'Yield' + Spot_Rates.keys()[0] + '.png'


def InflationCurve(publisher):
    inflationIndicatorObjects = []
    with open(pickledDataDirectoryPath + "/Inflation.dat", "rb") as f:
        for _ in range(pickle.load(f)):
            inflationIndicatorObjects.append(pickle.load(f))

    plt.ylabel('Consumer Price Index (%)')
    for element in inflationIndicatorObjects:
        element.refresh()
        element.Monthly['Taux'].plot(label=element.tag.replace('Inflation', ''), linewidth=0.4, marker='+')
        time.sleep(0.001)
    pickleObjectList(inflationIndicatorObjects, pickledDataDirectoryPath + "/Inflation.dat")
    plt.legend(loc=0, prop={'size': 6})
    plt.savefig(repositoryDirectory + "/Inflation_" + str(datetime.today().date()) + ".png", dpi=199)
    publisher.tweet_image("〽Inflation rates (basis = Consumer Price Index)〽",
                          repositoryDirectory + "/Inflation_" + str(datetime.today().date()) + ".png")


def compareYieldCurves(publisher):
    dataSpot = pd.read_csv(rateFileDirectory + '/Spot_Rates.csv', sep='\t')
    dataForward = pd.read_csv(rateFileDirectory + '/Instant_Forward_Rates.csv', sep='\t')
    EU_X_axis = [0.25, 0.5, 0.75, 1., 2., 3., 4., 5., 6.,
                 7., 8., 9., 10., 11., 12., 13., 14., 15.,
                 16., 17., 18., 19., 20., 21., 22., 23., 24.,
                 25., 26., 27., 28., 29., 30.]
    plt.plot(EU_X_axis, dataSpot.iloc[-1], label='EU spot Today', marker='+')
    plt.plot(EU_X_axis, dataSpot.iloc[-260], label='EU spot 1 year ago', marker='+')
    plt.plot(EU_X_axis, dataSpot.iloc[-1300], label='EU spot 5 years ago', marker='+')
    plt.plot(EU_X_axis, dataForward.iloc[-1], label='EU forward Today', ls='dotted')
    plt.plot(EU_X_axis, dataForward.iloc[-260], label='EU forward 1 year ago', ls='dotted')
    plt.plot(EU_X_axis, dataForward.iloc[-1300], label='EU forward 5 years ago', ls='dotted')
    plt.xticks(rotation='vertical', size=8)
    plt.legend(loc=4, prop={'size': 7})
    plt.savefig(repositoryDirectory + "/EUyieldCurves5years_" + str(datetime.today().date()) + ".png", dpi=199)
    plt.clf()
    dataSpotUS = pd.read_csv(rateFileDirectory + '/treasury_yields.csv', sep='\t')
    US_X_axis = [0.08333333, 0.16666667, 0.25, 0.5, 1.,
                 2., 3., 5., 7., 10.,
                 20., 30.]
    plt.plot(US_X_axis, dataSpotUS.iloc[-1][1:], label='US treasury yield Today', marker='+')
    plt.plot(US_X_axis, dataSpotUS.iloc[-260][1:], label='US treasury yield 1 years ago', marker='+')
    plt.plot(US_X_axis, dataSpotUS.iloc[-1300][1:], label='US treasury yield 5 years ago', marker='+')
    plt.xticks(rotation='vertical', size=8)
    plt.legend(loc=4, prop={'size': 7})
    plt.savefig(repositoryDirectory + "/USyieldCurves5years_" + str(datetime.today().date()) + ".png", dpi=199)
    publisher.tweet_image("Yield curves the last 5 years",
                          [repositoryDirectory + "/EUyieldCurves5years_" + str(datetime.today().date()) + ".png",
                           repositoryDirectory + "/USyieldCurves5years_" + str(datetime.today().date()) + ".png"]
                          )


def governmentRateUpdate(publisher):
    with open(pickledDataDirectoryPath + "/Government.dat", "rb") as f:
            object=pickle.load(f)
    object.checkGovernmentRateChange(publisher)


"""
        MONTHLY UPDATES / PUBICATIONS
"""


def monthlyLaborReport(publisher):
    if datetime.today().day <= 7:
        publisher.publish_tweet(
            "Publication du Rapport mensuel sur l'emploi américain : " + "https://www.bls.gov/opub/mlr/")


def getEconomicSentiment(publisher):
    Link = "https://www.mql5.com/en/economic-calendar/european-union/zew-indicator-of-economic-sentiment"
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(Link, headers=headers)
    data = soup(result.content,'html5lib')
    actualDate = data.find("td", {"id": "actualValueDate"})['data-date'].replace(" ", "")
    if not datetime.fromtimestamp(int(actualDate)/1000).date() == datetime.today().date() :
        return
    nextDate = data.find("td",{"id":"nextValueDate"})['data-date'].replace(" ","")
    actualRow = data.findAll("div" , {"class":"event-table-history__item"})[0]
    actualNumber =  "".join(actualRow.find("div" , {"class":"event-table-history__actual green"}).find("span").text.split())
    previousNumber = "".join(actualRow.find("div" , {"class":"event-table-history__previous"}).text.split())
    publisher.publish_tweet(" ".join(["Zew indicator of economic sentiment :",actualNumber,"(Previous result :",previousNumber,")\nNext release",str(datetime.fromtimestamp(int(nextDate)/1000).date())]))
