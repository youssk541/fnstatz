from updates import *
import concurrent.futures
import sys
import os
def pickleObjectList(objectList,fileName):
    with open(fileName, "wb+") as f:
        pickle.dump(len(objectList), f)
        for value in objectList:
            pickle.dump(value, f)


def createObjects(listSymbols, listIndicatorObjects):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for indicator, boole in zip(listSymbols, executor.map(IndicatorObject, listSymbols)):
            listIndicatorObjects.append(boole)
    return listIndicatorObjects

def startUSRate():
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
        if(row):
            treasury_yields.loc[datetime.strptime(row[0].text, "%m/%d/%y")] = [floatify(element.text) for element in row[1:]]

    treasury_yields.to_csv(rateFileDirectory + '/treasury_yields.csv', sep='\t',mode='a', header=None)

def startEuropeanRateFile():
    link = 'https://sdw-wsrest.ecb.europa.eu/service/data/YC/B.U2.EUR.4F.G_N_A.SV_C_YM.?startPeriod=2020-01-01'
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

    # if not datetime.today().weekday() <= 4:  # If it's not a weekday, no update
    Spot_Rates.to_csv(rateFileDirectory + '/Spot_Rates.csv', sep='\t', mode='a',header=None)
    Instant_Forward_Rates.to_csv(rateFileDirectory + '/Instant_Forward_Rates.csv',mode='a' ,header=None)

def startup():
    sys.setrecursionlimit(0x100000)
    IndicesIndicatorObjects, CAC40ComponentObjects, SP500ComponentObjects, DAXComponentObjects, FTSEComponentObjects,Inflation_objets = [], [], [], [], [], []
    createObjects(Indices.keys(), IndicesIndicatorObjects)
    createObjects(listSP500, SP500ComponentObjects)
    createObjects(listCAC40, CAC40ComponentObjects)
    createObjects(listDAX, DAXComponentObjects)
    createObjects(listFTSE, FTSEComponentObjects)
    [Inflation_objets.append(InflationContainer(urlIndex)) for urlIndex in url_dict_inflation.keys()]
    governmentRateObject = governmentRateContainer()
    ####
    startUSRate()
    startEuropeanRateFile()
    pickleObjectList(IndicesIndicatorObjects, pickledDataDirectoryPath +"/Indices.dat")
    pickleObjectList(CAC40ComponentObjects, pickledDataDirectoryPath +"/CAC40.dat")
    pickleObjectList(DAXComponentObjects, pickledDataDirectoryPath +"/DAX.dat")
    pickleObjectList(FTSEComponentObjects, pickledDataDirectoryPath +"/FTSE.dat")
    pickleObjectList(SP500ComponentObjects, pickledDataDirectoryPath + "/SP500.dat")
    pickleObjectList(Inflation_objets, pickledDataDirectoryPath + "/Inflation.dat")
    pickleObjectList([governmentRateObject], pickledDataDirectoryPath + "/Government_Rates.dat")
    
if __name__=="__main__":
    print("################# Installing requirements #################")
    os.system("py -m pip install -r requirements.txt ")
    print("\n\n")
    print("################# Requirements installed #################")
    print("\n\n")
    print("################# Initializing stock objects (This step might take a minute) #################")
    startup()
    print("########################################################\n########################################################\n")
    print("################# Startup process finished #################")
    time.sleep(3)
    os.system("exit")
    
