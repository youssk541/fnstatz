from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
from datetime import timedelta
import pandas as pd
import html5lib
month_swap_dict={'janvier':'Jan',
                 'fÃ©vrier':'Feb',
                 'mars':'Mar',
                 'avril':'Apr',
                 'mai':'May',
                 'juin':'Jun',
                 'juillet':'Jul',
                 'aoÃ»t':'Aug',
                 'septembre':'Sep',
                 'octobre':'Oct',
                 'novembre':'Nov',
                 'dÃ©cembre':'Dec'
                 }
url_dict={'1week':"https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-1-semaine.aspx",
          '1month':"https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-1-mois.aspx",
          '3month':"https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-3-mois.aspx",
          '6month':"https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-6-mois.aspx",
          '12month':"https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-12-mois.aspx",
          'EONIA':"https://fr.global-rates.com/taux-de-interets/eonia/eonia.aspx"
        }
class rate_Container():
    def __init__(self,urlIndex):
        self.url=url_dict[urlIndex]
        self.data=self.scrape()
        self.Daily=self.getDaily()
        self.Monthly=self.getMonthly()
        self.Yearly=self.getYearly()

    def scrape(self):
        uClient=uReq(self.url)
        page = uClient.read()
        page_soup_html = soup(page, "html.parser")
        data=page_soup_html.findAll("tr", {"class":["tabledata1","tabledata2"]})
        return data

    def getDaily(self):
        df_daily=pd.DataFrame(columns=['Date','Taux'])
        for i in range(12):
            element=self.data[i].findAll('td')
            df_daily.loc[i]=[frenchDateToDatetime(element[0].text),element[1].text]
        self.Daily=df_daily
        return df_daily

    def getMonthly(self):
        df_monthly=pd.DataFrame(columns=['Date','Taux'])
        for i in range(12,24):
            element=self.data[i].findAll('td')
            df_monthly.loc[i%12]=[frenchDateToDatetime(element[0].text),element[1].text]
        return df_monthly

    def getYearly(self):
        df_yearly = pd.DataFrame(columns=['Date', 'Taux'])
        for i in range(24,36):
            element = self.data[i].findAll('td')
            df_yearly.loc[i%24] = [frenchDateToDatetime(element[0].text), element[1].text]
        return df_yearly

def frenchDateToDatetime(str):
    str = str.split(sep=" ")
    str[0], str[1] = str[1],str[0]
    str[0]= month_swap_dict[str[0]]
    return(datetime.strptime(str[0]+" "+str[1]+" "+str[2],'%b %d %Y'))

def getVstoxx():
    url='https://www.stoxx.com/index-details?symbol=V2TX'
    page=uReq(url).read()
    page_soup_html=soup(page,'html5lib')
    container=page_soup_html.find('tr', {'class' : 'last'})
    print(container)
    print(container.find('td',{'id':"overview-last-value"}))

# my_url='https://www.stoxx.com/index-details?symbol=V2TX'
# euribor_1week=rate_Container('1week')
# euribor_1month=rate_Container('1month')
# euribor_3month=rate_Container('3month')
# euribor_6month=rate_Container('6month')
# euribor_12month=rate_Container('12month')
# eonia=rate_Container('EONIA')


#Open connexion
# uClient=uReq(my_url)
# #save page
# # page=uClient.read()
# # page_soup_html=soup(page,"html.parser")
# # containers=page_soup_html.find_all("tr", {"class":["tabledata1","tabledata2"]})
# # contain=containers[0]
# # print(getWeekly(containers))
# # print(getMonthly(containers))
# # print(getYearly(containers))
# # print(datetime.strptime('Jun'+' 28 2018','%b %d %Y'))
# print(euribor_1week.Daily)
# print(euribor_1month.Daily)
# print(euribor_3month.Daily)
# print(euribor_6month.Daily)
# print(euribor_12month.Daily)
# print(eonia.Daily)
getVstoxx()


