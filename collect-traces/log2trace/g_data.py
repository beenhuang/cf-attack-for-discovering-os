# coding=utf-8

import sys
import getopt
import re
import os
import csv

from file_path import getAllNodeFilePath
from client_circuit import getClientCircDict
from relay_circuit import getRelayCircDict
    
def writeGenCirc(tag, cName, rName, circ, rCircDict, outFileName):
    oFilePath = os.path.join(os.pardir, 'raw_data', 'general_traffic', f'general({outFileName}).csv')
    
    with open(oFilePath,"a") as f:    
        w = csv.writer(f, delimiter=',')
        w.writerow([f'{cName}', f'{rName}', f'{circ}', f'{tag}']+rCircDict[circ])

def runHousekeeping(circ, cName, cCircDict, rCircDict):
    # 
    clist = cCircDict[cName]
    clist.remove(circ)
    
    if not len(clist): # list is empty.
        del cCircDict[cName]
    
    # relay删除匹配的circuit
    del rCircDict[circ]

def filterGenCirc(rCircDict):
    for circ in list(rCircDict.keys()):
        if len(rCircDict[circ]) < 9000:
            del rCircDict[circ]        
        
def matchCirc(cCircDict, rFilePath, outFileName):
    print(f'[6] matchCirc(): start to create relay circuits one by one.')
    
    # 
    for rfp in rFilePath:
        # get relay name.
        rName = rfp.split('/')[-2]
        
        # get relay's all circuits with cell data.
        rCircDict = getRelayCircDict(rfp)
        filterGenCirc(rCircDict)  # 只保留general circuits.
        rCircList = rCircDict.keys()
        
        if not list(rCircList): # relay circuit list is empty.
            print(f'{rName} circuit list is empty.')
            continue
        
        # 
        for cName,cCircList in cCircDict.items():
            # 
            commonCirc = [val for val in cCircList if val in rCircList]
            for circ in commonCirc:
                writeGenCirc('general', cName, rName, circ, rCircDict, outFileName)
                runHousekeeping(circ, cName, cCircDict, rCircDict)
        print(f'{rName} has done.')          

def extractGenData(inFolderPath, outFileName):
    print('[3] extractGenData(): starting general mode.')  
                  
    # [4]  get all node' file paths.             
    cFilePath, rFilePath = getAllNodeFilePath(inFolderPath)
    
    # [5] get all clients' circuit
    cCircDict = getClientCircDict(cFilePath, 'general')
    print(f'[5] getClientCircDict(): created general circuit list of all clients.')
    
    # [6] get relay circuit and match to the client circuits
    matchCirc(cCircDict, rFilePath, outFileName)


