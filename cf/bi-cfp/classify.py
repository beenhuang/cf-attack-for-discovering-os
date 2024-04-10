#!/usr/bin/env python3

"""
<file>    classify.py
<brief>   classify website fingerprints.
"""

import os
import sys
import time
import pickle
import random
import logging
import argparse
from os.path import join, abspath, dirname, pardir, exists, basename
from collections import Counter
import numpy as np
from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE, SVMSMOTE, ADASYN, SMOTENC
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from rf_classifier import train_cf, test_cf, cm_plot2
from metrics import cw_score


def main(X, y, res_path):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random.randint(0,10000), stratify=y)
    logger.info(f"X_train: {len(X_train)}, X_test: {len(X_test)}")

    # 1. training
    model= train_cf(X_train, y_train)
    logger.info(f"[TRAINED] classifer of cf.")

    # 2. test
    y_pred = test_cf(model, X_test)
    logger.info(f"[GOT] predicted labels from test samples.")


    # 3. get metrics value
    lines = cw_score(y_test, y_pred)

    # 4. confusion matrix
    cm_plot2(y_test, y_pred, file=None)
  
    # save the results
    with open(res_path, "w") as f:
        f.writelines(lines)

# logger and arguments
def logger_and_arguments():  
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S") # get logger
    logger = logging.getLogger()
    
    parser = argparse.ArgumentParser() # parse arugment
    parser.add_argument("--out", required=True, help="save the result")
    parser.add_argument("--class", required=True, help="classes")
    args = vars(parser.parse_args())

    return logger, args

if __name__ == "__main__":
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    cur_time = time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())
    logger, args = logger_and_arguments()
    logger.info(f"Arguments:{args}")

    res_dir = join(BASE_DIR, "bi-cfp","res")
    if not exists(res_dir):
        os.makedirs(res_dir)

    with open(join(BASE_DIR, "bi-cfp", "feature", "feature.pkl"), "rb") as f:
        X, y = pickle.load(f) # load X, y


        if int(args["class"]) == 2:
            y = [0 if e == 1 or e == 3 else e for e in y]
            y = [1 if e == 2 or e == 4 else e for e in y]
        sm = SMOTE(random_state=random.randint(0,10000))
        X, y = sm.fit_resample(X, y)
        print(Counter(y))
        logger.info(f"X:{np.array(X).shape}, y:{np.array(y).shape}")
        logger.info(f"labels:{Counter(y)}")

    # main function    
    res_path = join(res_dir, cur_time+"_"+args["out"]+".txt")
    main(X, y, res_path) 

    logger.info(f"Classification completed!")
