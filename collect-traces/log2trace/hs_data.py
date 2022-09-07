# coding=utf-8

import os
import csv

from file_path import getAllNodeFilePath2
from client_circuit import getClientCircDict2
from hs_circuit import getHsCircList2
from relay_circuit import getRelayCircDict   

def filterCirc(rCircDict):
    for circ in list(rCircDict.keys()):
        if len(rCircDict[circ]) < 9000:
            del rCircDict[circ] 

def runHousekeeping(circ, cName, cCircDict, rCircDict):
    # 
    clist = cCircDict[cName]
    clist.remove(circ)
    
    if not len(clist): # list is empty.
        del cCircDict[cName]
    
    # 
    del rCircDict[circ]
    
def runHousekeeping2(circ, hsCircList, rCircDict):
    hsCircList.remove(circ)
    del rCircDict[circ]              

def writeCirc(tag, cName, rName, circ, rCircDict, outFileName):   
    oFilePath = os.path.join(os.pardir, 'raw_data', 'hs_traffic', f'{outFileName}.csv')

    with open(oFilePath, 'a') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow([f'{cName}', f'{rName}', f'{circ}', f'{tag}']+rCircDict[circ])

def matchClientCirc(tag, cCircDict, rName, rCircDict, outFileName):
    if not cCircDict.keys():
        return
        
    rCircList = rCircDict.keys()
    
    for cName in list(cCircDict.keys()):
        # 
        cCircList = cCircDict[cName]
            
        # 
        commonCirc = [val for val in cCircList if val in rCircList]
        for circ in commonCirc:
            writeCirc(tag, cName, rName, circ, rCircDict, outFileName)
            runHousekeeping(circ, cName, cCircDict, rCircDict)

def matchHsCirc(tag, hsCircList, rName, rCircDict, outFileName):
    if not len(hsCircList):
        return
    
    rCircList = rCircDict.keys()
    
    # 
    commonCirc = [val for val in hsCircList if val in rCircList]
    for circ in commonCirc:
        writeCirc(tag, 'HS', rName, circ, rCircDict, outFileName)
        runHousekeeping2(circ, hsCircList, rCircDict)

def matchCirc(ipClientDict, rpClientDict, ipHsCircList, rpHSCircList, rFilePath, outFileName):
    print(f'[7] matchCirc(): start to create relay circuits one by one.')
    
    # 
    for rfp in rFilePath:
        # get relay name.
        rName = rfp.split('/')[-2]
        
        # 
        rCircDict = getRelayCircDict(rfp)

        # match IP circuits.
        matchClientCirc('IpClient', ipClientDict, rName, rCircDict, f'IP_Client({outFileName})')
        matchHsCirc('IpHS', ipHsCircList, rName, rCircDict, f'IP_HS({outFileName})')
        
        filterCirc(rCircDict)  # 
        if not list(rCircDict.keys()): # relay circuit list is empty.
            print(f'[8] matchCirc(): {rName} circuit list is empty.')
            continue
            
        # match RP cricuits.
        matchClientCirc('RpClient', rpClientDict, rName, rCircDict, f'RP_Client({outFileName})')
        matchHsCirc('RpHS', rpHSCircList, rName, rCircDict, f'RP_HS({outFileName})')
        
        print(f'[8] matchCirc(): {rName} has done.')      
        
def extractHsData(inFolderPath, outFileName):
    print('[3] extractHsData(): start HS mode.')
    
    # [4] get all nodes' file paths.
    cFilePath, rFilePath, hsFilePath = getAllNodeFilePath2(inFolderPath)
 
    # [5] get IP and RP circuit data of both clients and HS.
    ipClientDict, rpClientDict = getClientCircDict2(cFilePath, 'IpClient', 'RpClient')
    ipHsCircList, rpHSCircList  = getHsCircList2(hsFilePath, 'IpHS', 'RpHS')
    
    # [6] get relay circ data and match with client or HS circID.
    matchCirc(ipClientDict, rpClientDict, ipHsCircList, rpHSCircList, rFilePath, outFileName) 
        
    
    
    
