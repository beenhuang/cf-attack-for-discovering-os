# coding=utf-8

from config import getParameter
from g_data import extractGenData
from hs_data import extractHsData

# python3 run.py -i /User/tornet0.01 -o seed1 -m gen
# python3 run.py -i /User/tornet0.01-hs -o seed1 -m hs

def run_extractor():
    print('[1] runExtractor(): start the program.')
    
    # [2] get parameters.
    inFolderPath, outFileName, mode = getParameter()

    if mode == 'hs':
        extractHsData(inFolderPath, outFileName)
    else:
        extractGenData(inFolderPath, outFileName)
        
    print('[Done] runExtractor(): It has done successfully. ^.^')

run_extractor()    