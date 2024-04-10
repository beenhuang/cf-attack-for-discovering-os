#!/usr/bin/env python3

"""
<file>    rf_classifier.py
<brief>   random forest classifier
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt

# training
def train_cf(X_train, y_train, trees=100, crit="gini"):
    model = RandomForestClassifier(n_estimators=trees, criterion=crit)
    model.fit(X_train, y_train)

    return model

# test
def test_cf(model, X_test):
    y_pred = model.predict(X_test)

    return y_pred

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
    #disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Client-side','OS-side'])

    disp.plot()
    plt.savefig('2-class.jpg', dpi=500, bbox_inches='tight')
    plt.show()
    #plt.savefig(file)    