#!/usr/bin/env python3

"""
<file>    run_cf.py
<brief>   Huang's circuit fingerprinting attack
"""

import argparse
import os
import sys
import csv
import time
import pickle
import logging
import numpy as np
from os.path import join, basename, abspath, splitext, dirname, pardir, isdir
import multiprocessing as mp

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier

from exfeature import extract_features


# CONSTANTS
MODULE_NAME = basename(__file__)
CURRENT_TIME = time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())

BASE_DIR = abspath(join(dirname(__file__)))
INPUT_DIR = join(BASE_DIR)
OUTPUT_DIR = join(BASE_DIR, "result")


RANDOM_STATE = 247
# Random Forest's hyperparameters:
TREES = 30
CRITERION = "gini"


# constants
DIRECTION_OUT = 1.0
DIRECTION_IN = -1.0

# create logger
def get_logger():
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    return logger


# parse arugment
def parse_arguments():
    # argument parser
    parser = argparse.ArgumentParser(description="cf")

    # 1. INPUT: load ds-*.pkl dataset
    parser.add_argument("-i", "--in", required=True, metavar="<trace file directory>", help="load trace data")
    # 2. OUTPUT: save overhead in the overhead-*.txt file
    parser.add_argument("-o", "--out", required=True, metavar="<result-file>", help="save results in the text file.")

    args = vars(parser.parse_args())

    return args

#
def generate_feature_vectors(data_dir):
    # gen files
    files = [join(data_dir, "general-trace", file) for file in os.listdir(join(data_dir, "general-trace"))]
    # hs files
    hs_files = [join(data_dir, "hs-trace", file) for file in os.listdir(join(data_dir, "hs-trace"))]
    files.extend(hs_files)

    X, y = [], []
    for file in files: # each file
        with open(file, "r") as f:
            reader = csv.reader(f, delimiter=",")

            for trace in reader:
                feature, label = extract_features(trace)

                X.append(feature)
                y.append(label)   

    #print(f"X: {X}")
    #print(f"y: {y}")
    
    return X, y


# training
def train_cf(X_train, y_train):
    model = RandomForestClassifier(n_estimators=TREES, criterion=CRITERION)
    model.fit(X_train, y_train)

    return model

# test
def test_cf(model, X_test):
    y_pred = model.predict(X_test)

    return y_pred

def get_closeworld_score(y_true, y_pred):
    # accuracy
    accuracy = accuracy_score(y_true, y_pred)
    # precision      
    precision = precision_score(y_true, y_pred, average="macro")
    # recall
    recall = recall_score(y_true, y_pred, average="macro")
    # F-score
    f1 = 2*(precision*recall) / float(precision+recall)

    lines = []
    lines.append(f"accuracy: {accuracy}\n")
    lines.append(f"precision: {precision}\n")
    lines.append(f"recall: {recall}\n")
    lines.append(f"F1: {f1}\n")
    return lines


# MAIN function
def main():
    logger = get_logger()
    logger.info(f"{MODULE_NAME}: start to run.")

    # parse arguments
    args = parse_arguments()
    logger.info(f"Arguments: {args}")

    # load dataset&labels
    data_dir = join(INPUT_DIR, args["in"])
    X, y = generate_feature_vectors(data_dir)
    logger.info(f"[LOADED] dataset&labels, length: {len(X)}, {len(y)}")

    # split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    print(f"X_train: {len(X_train)}, X_test: {len(X_test)}")

    # training
    model= train_cf(X_train, y_train)
    logger.info(f"[TRAINED] random_forest model of cf.")

    # test
    y_pred = test_cf(model, X_test)
    logger.info(f"[GOT] predicted labels of test samples.")
    
    # get metrics value
    lines = get_closeworld_score(y_test, y_pred)
    logger.info(f"[CALCULATED] close-world scores.")
    
    with open(join(OUTPUT_DIR, f"{CURRENT_TIME}_{args['out']}.txt"), "w") as f:
        f.writelines(lines)
        logger.info(f"[SAVED] metrics scores in the {args['out']}.txt")

    logger.info(f"{MODULE_NAME}: complete successfully.\n")


if __name__ == "__main__":
    sys.exit(main())


