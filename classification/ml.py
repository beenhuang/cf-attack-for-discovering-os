#!/usr/bin/env python3

import argparse
import os
import sys
import pickle
import warnings

import matplotlib.pyplot as plt
from collections import Counter

from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE, SVMSMOTE, ADASYN, SMOTENC
from imblearn.combine import SMOTEENN, SMOTETomek

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, cross_validate

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score, precision_recall_fscore_support
from sklearn import metrics


# ignore warning
warnings.filterwarnings("ignore")

# argument parser:
parser = argparse.ArgumentParser()

# 1. input: 
parser.add_argument("--in", required=True, 
                    help="input")

# 2. output: 
parser.add_argument("--out", required=True, 
                    help="output")

# 3. sampling strategy:
parser.add_argument("--sampling", required=True,
                    default="random", help="over-sampling strategy")

# 4. random state:
parser.add_argument("--random_state", required=True, type=int,
                    default="99", help="random state")

# 5. classification model:
parser.add_argument("--model", required=True, help="classification model")

# 6. get optimal hyperparameters:
parser.add_argument("--hyper", required=False, action="store_true", 
                    default=False, help="find optimal hyperparams")

# 7. label:
parser.add_argument("--label", required=False, type=int, 
                    default=2, help="label")

# 8. parameter_1 of classification model:
parser.add_argument("--param1", required=False, type=int, help="parameter 1")

# 9. parameter_2 of classification model:
parser.add_argument("--param2", required=False, type=str, default="", help="parameter 2")

args = vars(parser.parse_args())

# over sampling
def perform_over_sampling(X, y, strategy, rs):

    # random over sampling
    if strategy == 'random' :
        ros = RandomOverSampler(random_state=rs)
        X_res, y_res = ros.fit_resample(X, y)

    elif strategy == 'smote' :
        sm = SMOTE(random_state=rs)
        X_res, y_res = sm.fit_resample(X, y)

    elif strategy == 'svmsmote' :
        svmsm = SVMSMOTE(random_state=rs)
        X_res, y_res = svmsm.fit_resample(X, y)

    elif strategy == 'border' :   
        blsm = BorderlineSMOTE(random_state=rs)
        X_res, y_res = blsm.fit_resample(X, y)

    elif strategy == 'tomek' :    
        smt = SMOTETomek(random_state=rs)
        X_res, y_res = smt.fit_resample(X, y)

    # unrecognized
    else :
        sys.exit(f"[ERROR] unrecognized strategy : [{strategy}] ")
    

    return X_res, y_res


# in order to find the optimal hyperparameters
def get_optimal_hyperparams(X, y, model):

    print(f"[{model.upper()}] get optimal hyperparameters")

    # svm
    if model == "svm" :
        hyperparams = {'svc__C':[64, 128, 256], 'svc__gamma':[32, 64, 128]}
        pipline = Pipeline([('standardscaler', StandardScaler()), ('svc', SVC(kernel='rbf'))])
        clf = GridSearchCV(pipline, param_grid=hyperparams, n_jobs=-1, cv=5)
        clf.fit(X, y)

    # random forest
    elif model == "rf" :
        hyperparams = {'criterion':('gini', 'entropy'), 'n_estimators':[30, 40, 50]}
        clf = GridSearchCV(RandomForestClassifier(), hyperparams, n_jobs=-1, cv=5)
        clf.fit(X, y)

    # xgboost
    elif model == "xgboost" :
        hyperparams = {'n_estimators':[20, 30, 40]}
        clf = GridSearchCV(XGBClassifier(), hyperparams, n_jobs=-1, cv=5)
        clf.fit(X, y)

    # unrecoginized model
    else :
        sys.exit(f"[ERROR] unrecognized classification model : [{model}]")
    
    # write to txt file
    lines = []

    lines.append(f"{model} best_params_: {clf.best_params_} \n")
    lines.append(f"{model} best_score_: {clf.best_score_} ")


    return lines


#
def get_cross_val_score(X, y, clf, cv):
    
    # 
    lines = []

    lines.append(f"----- 10-fold cross-validation ----- \n")

    # [1] precision_weighted
    scores = cross_val_score(clf, X, y, cv=cv, scoring='precision_weighted')
    lines.append(f"precision_weighted: {scores} \nprecision_weighted mean: {scores.mean()}\n\n")

    # [2] recall_weighted
    scores = cross_val_score(clf, X, y, cv=cv, scoring='recall_weighted')
    lines.append(f"recall_weighted: {scores} \nrecall_weighted mean: {scores.mean()}\n\n")

    # [3] f1_weighted
    scores = cross_val_score(clf, X, y, cv=cv, scoring='f1_weighted')
    lines.append(f"f1_weighted: {scores} \nf1_weighted mean: {scores.mean()}\n\n")

    return lines

#
def get_70_30_split_score(X_train, X_test, y_train, y_test, clf, rs):

    lines = []

    lines.append(f"\n----- 70-30 split ----- \n")

    # fit
    clf.fit(X_train, y_train)
    
    #
    lines.append(f"precision: {precision_score(y_test, clf.predict(X_test), average='weighted')} \n")
    lines.append(f"recall: {recall_score(y_test, clf.predict(X_test), average='weighted')} \n")
    lines.append(f"f1_score: {f1_score(y_test, clf.predict(X_test), average='weighted')}")


    return lines

#
def get_confusion_matrix_plot(X, y, clf, label, file):

    cm = confusion_matrix(y, clf.predict(X))

    if label == 2 :
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Client','Onion_Service'])
    elif label == 5 :
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['gen','Client-IP','Client-RP','OS-IP','OS-RP'])  
    else :
        sys.exit(f"[ERROR] unrecognized label value : [{label}]")

    disp.plot()
    #plt.show()
    plt.savefig(os.path.join(os.getcwd(), "results", "figures", file))

# 
def run_classifier(X, y, model, rs, param1, param2, label, file):

    lines = []

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rs, train_size=0.7)


    if model == "svm" :
        print(f"[{model.upper()}] C: {param1}, gamma: {param2}, random_state: {rs}")
        clf = Pipeline([('standardscaler', StandardScaler()), ('svc', SVC(kernel='rbf', C=param1, gamma=int(param2)))])
    
    elif model == "rf" :
        print(f"[{model.upper()}] n_estimators: {param1}, criterion: {param2}, random_state: {rs}")
        clf = RandomForestClassifier(n_estimators=param1, criterion=param2)
        
    elif model == "xgboost" :
        print(f"[{model.upper()}] n_estimators: {param1}, random_state: {rs}")
        #clf = XGBClassifier(n_estimators=20, objective='binary:logistic')
        clf = XGBClassifier(n_estimators=param1)

    else :
        sys.exit(f"[ERROR] unrecognized classification model : [{model}]")
         

    # [1] get cross-validation scores
    lines = get_cross_val_score(X, y, clf, 10)

    # [2] get 70-30 split scores
    lines.extend(get_70_30_split_score(X_train, X_test, y_train, y_test, clf, rs)) 

    # [3] confusion matrix plot
    get_confusion_matrix_plot(X_test, y_test, clf, label, file)
    

    return lines

#     
def main():

    print(f"---------  [{os.path.basename(__file__)}]: start to run [{args['in']}]  ---------")

    # [1] load the pickle file
    with open(os.path.join(os.getcwd(), "feature", args["in"]), "rb") as f:
        X, y = pickle.load(f)

    print(f"[LOADED] {args['in']} file")


    # [2] over-sampling :
    X_res, y_res = perform_over_sampling(X, y, args["sampling"], args["random_state"])

    print(f"[RESAMPLED] dataset: [{Counter(y_res)}],\n\t    original dataset: [{Counter(y)}]")

    
    # [3] get optimal hyperparameters
    if args["hyper"] :
        lines = get_optimal_hyperparams(X_res, y_res, args["model"])
        file = os.path.join(os.getcwd(), "results", "hyperparameters", args["out"]+".txt")
    
    # [3] classification
    else :    
        lines = run_classifier(X_res, y_res, args["model"], args["random_state"], args["param1"], args["param2"], args["label"], args["out"])
        file = os.path.join(os.getcwd(), "results", args["out"]+".txt")


    # [4] write to *.txt file
    with open(file, "w") as f:
        f.writelines(lines)

        print(f"[SAVED] scores to the [{args['out']}] file.")
    
    
    print(f"-------  [{os.path.basename(__file__)}]: completed successfully  -------\n\n")


if __name__ == "__main__":
    main()    