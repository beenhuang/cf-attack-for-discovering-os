# coding=utf-8
#
# $[%u,%d:0,-1]
#
# rCircDict = {'circ1':[cell1, cell2, ...], 'circ2':[cell1, cell2, ...], ...}
#

import re

def getRelayCircDict(rFilePath: str) -> dict:
    rCircDict = {}
    
    regexp = re.compile('<HUANG')
    regexp2 = re.compile('\$\[.+\]')

    with open(rFilePath,'r') as f:
        for line in f.readlines():
            if regexp.search(line):
                circ = regexp2.search(line)
                cell = re.sub("[\$\[\]]+", "", circ.group()).split(",")
                
                # cell[0],cell[1],cell[2]: circ_ID, cell_type, direction
                if cell[0] not in rCircDict:
                    rCircDict[cell[0]] = [f'{cell[1]}:{cell[2]}']
                else:
                    rCircDict[cell[0]].append(f'{cell[1]}:{cell[2]}')
                    
    return rCircDict                                     
