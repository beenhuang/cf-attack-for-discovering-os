#!/usr/bin/env python3

"""
<file>    metrics.py
<brief>   open-world, closed-world metrics
"""

from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, f1_score, precision_recall_curve, RocCurveDisplay, recall_score, PrecisionRecallDisplay

# closed-world score 
# average: ['micro', 'macro', 'samples', 'weighted', None]
def cw_score(y_true, y_pred, avg='weighted'):
    acc = accuracy_score(y_true, y_pred)  
    pre = precision_score(y_true, y_pred, average=avg)
    rec = recall_score(y_true, y_pred, average=avg)
    f1 = f1_score(y_true, y_pred, average=avg)

    y_true_pred = list(zip(y_true, y_pred))
    pred_incorrect = [x for x in y_true_pred if x[0] != x[1]]
    sorted_incorrect = sorted(pred_incorrect, key=lambda x:x[0]) 

    return [f"Accuracy:{acc}\n",
             f"Precision:{pre}\n",
             f"Recall:{rec}\n",
             f"F1:{f1}\n\n",
             f"incorrect prediction:{sorted_incorrect}\n\n"]
             