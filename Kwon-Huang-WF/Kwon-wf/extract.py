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
import multiprocessing as mp
from os.path import abspath, dirname, join, basename, pardir, exists, splitext

from kwon_feature import kwon_feature

# create logger
def get_logger():
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    return logger

# parse arugment
def parse_arguments():
    # create argument parser
    parser = argparse.ArgumentParser(description="cf")

    # INPUT
    parser.add_argument("-i", "--in", required=True, help="load trace data")

    # parse arguments
    args = vars(parser.parse_args())

    return args

def preprocess(trace):
    times = []
    dirs = []
    
    for x in trace:
        if x == "\n":
            continue
        x = x.split("\t")
        times.append(float(x[0]))
        dirs.append(int(x[1]))    

    return times, dirs

def extract(data_dir, feature_dir, file, umon_label=100):
    # 1. read a trace file.
    file_path = join(data_dir, file)
    with open(file_path, "r", errors="ignore") as f:
        trace = f.readlines() 
        #print(trace)

    # 2. preprocess the trace.    
    times, directions = preprocess(trace) 

    # 3. get feature vector
    feature = kwon_feature(times, directions) 

    
    # 1. get label
    print(f"feature_fname: {file}")
    if "-" in file:
        label = int(file.split("-")[0])
    else:
        label = umon_label

    # save the feature from the trace
    feature_path = join(feature_dir, file)
    with open(feature_path, "w") as f:
        for element in feature:
            f.write(f"{element}\n")

    return (feature, label)   

def main(data_dir, feature_dir, feature_pickle="feature.pkl"):
    flist = os.listdir(data_dir)
    params = [[data_dir, feature_dir, f] for f in flist]

    with mp.Pool(mp.cpu_count()) as pool:
        result = pool.starmap(extract, params)

    X, y = zip(*result) 

    with open(join(feature_dir, feature_pickle), "wb") as f:
        pickle.dump((X, y), f)    
    
    #logger.debug(f"X: {X}")
    #logger.debug(f"y: {y}")
    
    logger.info(f"Complete")     

if __name__ == "__main__":
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    MAIN_DATA_DIR = join(BASE_DIR, "data")
    MAIN_FEATURE_DIR = join(BASE_DIR, "Kwon-wf","feature")

    try:
        logger = get_logger()
        args = parse_arguments()
        logger.info(f"{basename(__file__)} -> Arguments: {args}")

        data_dir = join(MAIN_DATA_DIR, args["in"])

        if not exists(MAIN_FEATURE_DIR):
            os.makedirs(MAIN_FEATURE_DIR)

        feature_dir = join(MAIN_FEATURE_DIR, args["in"])
        if not exists(feature_dir):
            os.makedirs(feature_dir)            

        main(data_dir, feature_dir)    

    except KeyboardInterrupt:
        sys.exit(-1)    
