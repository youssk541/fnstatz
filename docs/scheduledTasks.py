from docs.updates import *
import schedule
from timeloop import Timeloop
from docs.tweepy_streamer import TwitterClient

tl = Timeloop()  # Handles periodic executions in multiple threads
publisher = TwitterClient()

schedule.every().saturday.at("22:20").do(YieldCurve, publisher)
schedule.every().saturday.at("19:00").do(InflationCurve, publisher)
schedule.every().sunday.at("12:00").do(compareYieldCurves, publisher)
schedule.every().friday.at("20:55").do(monthlyLaborReport, publisher)
schedule.every().tuesday.at("11:30").do(getEconomicSentiment,publisher)
schedule.every().day.at("15:00").do(governmentRateUpdate,publisher)
schedule.every().day.at("17:30").do(dailyUpdateEuropean, publisher)
schedule.every().day.at("22:30").do(dailyUpdateCommodities, publisher)
schedule.every().day.at("22:10").do(dailyUpdateAmerican, publisher)
schedule.every().day.at("22:00").do(rateUpdate)
schedule.every().day.at("17:30").do(endOfDayEuropeanStockMarket, publisher)
schedule.every().day.at("22:30").do(endOfDayUsStockMarket, publisher)

schedule.every(15).minutes.do(highFrequencyUpdateEuropeanStocks, publisher)
schedule.every(15).minutes.do(highFrequencyUpdateAmericanStocks, publisher)

if __name__=="__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)