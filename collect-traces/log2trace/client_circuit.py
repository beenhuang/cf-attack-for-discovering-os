# coding=utf-8
#
# $[IpClient,%u,%s], $[RpClient,%u], $[general,%u,%d]
#
# cCircDict = {'name1':[circ1, circ2, ...], 'name2':[circ1, circ2, ...], ...}
# 

import re

def getC1CircList(c1, tag):
    circList = []
    
    regexp = re.compile('HUANG')
    regexp2 = re.compile('\$\[.+\]')
    
    with open(c1, 'r') as f:
        for line in f.readlines():
            if regexp.search(line):
                circ = regexp2.search(line)
                dList = re.sub("[\$\[\]]+", "", circ.group()).split(",")
            
                # dList[0] is a tag, and dList[1] is a circ ID
                if dList[0] == tag and dList[1] not in circList:   
                    circList.append(dList[1])
    
    return circList     
    
def getClientCircDict(cFilePath, tag):
    cCircDict = {}
    
    for c1 in cFilePath:
        # get client name.
        cName = c1.split('/')[-2]
        
        # get cName's circuit list.
        cCircDict[cName] = getC1CircList(c1, tag)
    
    return cCircDict
    
def getClientCircDict2(cFilePath, tag1, tag2):
    ipClientDict = getClientCircDict(cFilePath, tag1)
    rpClientDict = getClientCircDict(cFilePath, tag2)
    
    print(f'[5] getClientCircDict2(): created [{tag1}] and [{tag2}] circuit list of all clients.')
    return ipClientDict, rpClientDict
         
        