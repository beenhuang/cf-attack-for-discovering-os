#!/usr/bin/env python3

"""
<file>    exfeature.py
<brief>   extract features from a trace using cf_feature.py
"""

import argparse
import os
import csv
import sys
import logging
import pickle
from os.path import abspath, dirname, join, basename, pardir, exists, splitext

from kwon_feature import kwon_feature


def get_label(trace):
    if(trace[3] == "general"):
        label = 0
    elif(trace[3] == "RpClient"):
        label = 1
    elif(trace[3] == "RpHS"):
        label = 2      
    elif(trace[3] == "IpClient"):
        label = 3
    elif(trace[3] == "IpHS"):
        label = 4
    else:
        print(f"unrecognized label: {trace[3]}")  

    return label          

def preprocess(trace):
    directions = trace[4:]

    good_trace = [[0, int(x.split(":")[2])] for x in directions]

    return good_trace

def main(data_dir, feature_dir, feature_pickle="feature.pkl"):
    # general/HS files
    flist = [join(data_dir, "general-trace", file) for file in os.listdir(join(data_dir, "general-trace"))]
    hs_files = [join(data_dir, "hs-trace", file) for file in os.listdir(join(data_dir, "hs-trace"))]
    flist.extend(hs_files)

    # gen, C-RP, H-RP, C-IP, H-IP
    max_inst = [0, 0, 0, 0, 0] 

    X, y = [], []
    for file in flist: 
        with open(file, "r") as f:
            reader = csv.reader(f, delimiter=",")

            for trace in reader:
                # get feature & label
                good_trace = preprocess(trace)
                feature = kwon_feature(good_trace)
                label = get_label(trace)
                
                # save the feature of one trace
                feature_path = join(feature_dir, f"{label}-{max_inst[label]}")
                with open(feature_path, "w") as f:
                    for e in feature:
                        f.write(f"{e}\n")

                logger.info(f"{label}-{max_inst[label]}")        

                # add 1        
                max_inst[label] += 1

                X.append(feature)
                y.append(label)   

    # save feature pickle file
    with open(join(feature_dir, feature_pickle), "wb") as f:
        pickle.dump((X, y), f)        

    logger.info(f"Complete") 

# create logger
def get_logger():
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    return logger

# parse arugment
def parse_arguments():
    # create argument parser
    parser = argparse.ArgumentParser(description="Kwon_cf")

    # INPUT
    parser.add_argument("-i", "--in", required=True, help="load trace data")

    # parse arguments
    args = vars(parser.parse_args())

    return args

if __name__ == "__main__":
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    MAIN_DATA_DIR = join(BASE_DIR)
    MAIN_FEATURE_DIR = join(BASE_DIR, "Kwon-cf","feature")

    try:
        logger = get_logger()
        args = parse_arguments()
        logger.info(f"{basename(__file__)} -> Arguments: {args}")

        data_dir = join(MAIN_DATA_DIR, args["in"])

        if not exists(MAIN_FEATURE_DIR):
            os.makedirs(MAIN_FEATURE_DIR)

        main(data_dir, MAIN_FEATURE_DIR)    

    except KeyboardInterrupt:
        sys.exit(-1)    

