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
    pickleObjectList(IndicesIndicatorObjects, pickledDataDirectoryPath +"/Indices.dat")
    pickleObjectList(CAC40ComponentObjects, pickledDataDirectoryPath +"/CAC40.dat")
    pickleObjectList(DAXComponentObjects, pickledDataDirectoryPath +"/DAX.dat")
    pickleObjectList(FTSEComponentObjects, pickledDataDirectoryPath +"/FTSE.dat")
    pickleObjectList(SP500ComponentObjects, pickledDataDirectoryPath + "/SP500.dat")
    pickleObjectList(Inflation_objets, pickledDataDirectoryPath + "/Inflation.dat")
    pickleObjectList([governmentRateObject], pickledDataDirectoryPath + "/Government_Rates.dat")


if __name__== "__main__":
    startup()
    #
    # governmentRateObject = governmentRateContainer()
    # os.mkdir('bla')

