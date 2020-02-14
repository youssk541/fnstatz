from .updates import *
import schedule
from timeloop import Timeloop
from .tweepy_streamer import TwitterClient

tl = Timeloop()  # Handles periodic executions in multiple threads
publisher = TwitterClient()

schedule.every().saturday.at("22:20").do(YieldCurve, publisher)
schedule.every().saturday.at("22:30").do(InflationCurve,publisher)
schedule.every().friday.at("20:55").do(monthlyLaborReport, publisher)
schedule.every().day.at("17:30").do(dailyUpdateEuropean, publisher)
schedule.every().day.at("22:10").do(dailyUpdateCommodities, publisher)
schedule.every().day.at("22:15").do(dailyUpdateAmerican, publisher)
schedule.every().day.at("22:00").do(rateUpdate)
schedule.every().day.at("17:30").do(endOfDayEuropeanStockMarket, publisher)
schedule.every().day.at("22:30").do(endOfDayUsStockMarket, publisher)
schedule.every(15).minutes.do(highFrequencyUpdateEuropeanStocks, publisher)
schedule.every(15).minutes.do(highFrequencyUpdateAmericanStocks, publisher)