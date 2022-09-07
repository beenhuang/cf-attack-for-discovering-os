# coding=utf-8

import sys
import getopt

def getParameter(mode='general'):
    try:
        opts, args = getopt.getopt(sys.argv[1:],'i:o:m:',['input=', 'output=', 'mode='])
    except:
        print("[2] getParameter(): Parameter Error")
        
    for oName, oValue in opts:
        if oName in ['-i', '--input']:
            inFolderPath = oValue
        elif oName in ['-o', '--output']:
            outFileName = oValue
        elif oName in ['-m', '--mode']:
            mode = oValue
    
    print(f'[2] getParameter(): input={inFolderPath}, output={outFileName}, mode={mode}')        
    
    return inFolderPath, outFileName, mode