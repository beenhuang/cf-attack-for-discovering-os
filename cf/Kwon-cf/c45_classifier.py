#!/usr/bin/env python3

"""
<file>    C45_classifier.py
<brief>   C45 classifier
"""

from c45 import C45

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt

# training
def train_cf(X_train, y_train):
    model = C45()
    model.fit(X_train, y_train)

    return model

# test
def test_cf(model, X_test):
    y_pred = model.predict(X_test)

    return y_pred

# close-world score
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

#
def cm_plot(X, y, model, file=None):

    cm = confusion_matrix(y, model.predict(X))

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['General','Client-RP','OS-RP','Client-IP','OS-IP'])  
    #disp = ConfusionMatrixDisplay(confusion_matrix=cm)

    disp.plot()
    plt.show()
    #plt.savefig(file)

def cm_plot2(y_test, y_pred, file=None):
    cm = confusion_matrix(y_true=y_test, y_pred=y_pred)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['General','Client-IP','OS-IP','Client-RP','OS-RP'])  
    #disp = ConfusionMatrixDisplay(confusion_matrix=cm)

    disp.plot()
    plt.savefig('5-class.png', dpi=500, bbox_inches='tight')
    plt.show()
    #plt.savefig(file)

