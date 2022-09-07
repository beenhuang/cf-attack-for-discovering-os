# coding=utf-8
#
# $[RpHS,circID], $[IpHS,circID]
#
# cricList = [circ1, cric2, ...]
#

import re
    
def getHsCircList(hsFilePath, tag):
    circList = []
    
    regexp = re.compile('HUANG')
    regexp2 = re.compile('\$\[.+\]')
    
    with open(hsFilePath, 'r') as f:
        for line in f.readlines():
            if regexp.search(line):
                circ = regexp2.search(line)
                dList = re.sub("[\$\[\]]+", "", circ.group()).split(",")
                    
                if dList[0] == tag and dList[1] not in circList:   
                    circList.append(dList[1])
    
    return circList
    
def getHsCircList2(hsFilePath, tag1, tag2):
    ipHsCircList = getHsCircList(hsFilePath, tag1)
    rpHSCircList = getHsCircList(hsFilePath, tag2)  
    
    print(f'[6] getHsCircList2(): created [{tag1}] and [{tag2}] circuit list of a hidden server.')
    return ipHsCircList, rpHSCircList