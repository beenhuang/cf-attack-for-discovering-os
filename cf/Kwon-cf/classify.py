#!/usr/bin/env python3

"""
<file>    classify.py
<brief>   classify the dataset using xx_classifer.py model.
"""

import argparse
import os
import sys
import time
import pickle
import logging
import numpy as np
from os.path import join, basename, abspath, splitext, dirname, pardir, isdir, exists

from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE, SVMSMOTE, ADASYN, SMOTENC

from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt

from c45_classifier import train_cf, test_cf, get_closeworld_score, cm_plot2

from collections import Counter

# create logger
def get_logger():
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    return logger

def parse_arguments():
    parser = argparse.ArgumentParser(description="cf")
    parser.add_argument("-i", "--in", required=True, help="load feature.pkl file")
    parser.add_argument("-o", "--out", required=True, help="save results")
    args = vars(parser.parse_args())

    return args


# MAIN function
def main(X, y, result_path):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=247, stratify=y)
    logger.info(f"X_train: {len(X_train)}, X_test: {len(X_test)}")
    
    # 1. training
    model= train_cf(X_train, y_train)
    logger.info(f"[TRAINED] classifer of cf.")

    # 2. test
    y_pred = test_cf(model, X_test)
    logger.info(f"[GOT] predicted labels from test samples.")
    #logger.debug(f"y_pred: {y_pred}")
    
    # 3. get metrics value
    lines = get_closeworld_score(y_test, y_pred)

    # 4. confusion matrix
    cm_plot2(y_test, y_pred, file=None)

    #cm = confusion_matrix(y_true=y_test, y_pred=y_pred)

    #cm_display = ConfusionMatrixDisplay(cm, display_labels=["Client-side", "OS-side"])
    #cm_display = ConfusionMatrixDisplay(cm, display_labels=["Client-side", "OS-side"])
    #cm_display.plot()

    #plt.show()
    #plt.savefig('2-class.png', dpi=500, bbox_inches='tight')
    #plt.clf()


    # save the results
    with open(result_path, "w") as f:
        f.writelines(lines)

    logger.info(f"Complete!")


if __name__ == "__main__":
    CURRENT_TIME = time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())
    BASE_DIR = abspath(join(dirname(__file__)))
    FEATURE_DIR = join(BASE_DIR, "feature")
    RESULT_DIR = join(BASE_DIR, "result")

    logger = get_logger()
    args = parse_arguments()
    logger.info(f"{basename(__file__)} -> Arguments: {args}")

    feature_path = join(FEATURE_DIR, args["in"])
    with open(feature_path, "rb") as f:
        X, y = pickle.load(f)
        logger.info(f"[LOADED] dataset:{len(X)}, labels:{len(y)}")

        sm = SMOTE(random_state=100)
        X, y = sm.fit_resample(X, y)
        print(Counter(y))
        y = [0 if e == 1 or e == 3  else e for e in y]
        y = [1 if e == 2 or e == 4 else e for e in y]        

    if not exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
        
    result_path = join(RESULT_DIR, CURRENT_TIME+"_"+args["out"]+".txt")

    main(X, y, result_path)



