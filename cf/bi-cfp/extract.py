#!/usr/bin/env python3

"""
<file>    extract.py
<brief>   extract features
"""

import os
import csv
import sys
import pickle
import logging
import argparse
from os.path import abspath, dirname, pardir, exists, join, splitext

from bc_feature import get_feature


def preprocess(trace):
    directions = trace[4:]

    good_trace = [[int(x.split(":")[0]), int(x.split(":")[2])] for x in directions]

    return good_trace

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

# only need to change the extract function.
def extract(d_dir, f_dir, file, label_unmon=0):
    print(f"extracting:{file}", end="\r", flush=True)

    std_trace = Preprocess.standard_trace(d_dir, file, "\t") # get a standard trace.
    if std_trace == -1: # standard trace is empty.
        return (-1, -1)

    # feature & label
    feat = get_feature(std_trace)
    label = label_unmon if '-' not in file else int(file.split('-')[0])+1
    
    with open(join(f_dir, file),'w') as f: # save feature in the file
        for e in feat:
            f.write(f"{e}\n")

    return (feat, label)   
    
# main function
def main(d_dir, f_dir):
    # general/HS files
    flist = [join(d_dir, "general-trace", file) for file in os.listdir(join(d_dir, "general-trace"))]
    hs_files = [join(d_dir, "hs-trace", file) for file in os.listdir(join(d_dir, "hs-trace"))]
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
                feature = get_feature(good_trace)
                label = get_label(trace)
                
                # save the feature of one trace
                feature_path = join(f_dir, f"{label}-{max_inst[label]}")
                with open(feature_path, "w") as f:
                    for e in feature:
                        f.write(f"{e}\n")

                logger.info(f"{label}-{max_inst[label]}")        

                # add 1        
                max_inst[label] += 1

                X.append(feature)
                y.append(label)   

    # save feature pickle file
    with open(join(f_dir, "feature.pkl"), "wb") as f:
        pickle.dump((X, y), f)        

# logger and arguments
def logger_and_arguments():
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", required=True, help="dataset directory")
    args = vars(parser.parse_args())

    return logger, args


if __name__ == "__main__":
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    logger, args = logger_and_arguments()
    logger.info(f"Arguments:{args}")

    d_dir = join(BASE_DIR, args["in"])   
    f_dir = join(BASE_DIR, "bi-cfp", "feature")
    if not exists(f_dir):
        os.makedirs(f_dir)

    main(d_dir, f_dir) # main function

    logger.info(f"Feature extraction completed!")    
