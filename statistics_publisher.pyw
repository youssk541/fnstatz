from tweepy_streamer import TwitterClient
from pandas_datareader import data as pdr
from datetime import datetime
from datetime import timedelta
from math import log
from math import exp
import schedule
AvKey="KGGUWE9H179YXT4K" #USING ALPHAVANTAGE FOR HOURLY DATA

def getCac40():
    start = datetime.strftime(datetime.today() - timedelta(days=1), '%Y-%m-%d')
    end = datetime.strftime(datetime.today(), '%Y-%m-%d')
    dailyData = pdr.get_data_yahoo("^FCHI",  start=start,end=end)
    pctChangement=log(dailyData['close'][1]/dailyData['Close'][0],exp(1))*100
    textToPublish = "L'index du cac40 enregistre " + str(dailyData['Close'][1]) + " aujourd'hui soit " + str("{0:.2f}".format(pctChangement)) + "% par rapport à hier"
    publisher = TwitterClient()
    publisher.publish_tweet(textToPublish)


def test():
    with open('tweets.txt','a') as file:
        print('Filename:',  file=file)
if __name__ == '__main__':
    schedule.every().day.at("18:26").do(getCac40())
    while True:
        schedule.run_pending()
