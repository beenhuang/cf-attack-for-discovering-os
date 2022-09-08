#
# classification
#
#
# [1] find optimal hyperparameters:
# ml.py --in <~/feature/*.pkl>  --out <~/results/hyperpameters/*> --hyper --sampling [random/smote/svmsmote/border/tomek] --random_state 99 --model [svm/rf/xgboost]
#
# [2] classification
# ml.py --in <~/feature/*.pkl>  --out <~/results/*> --label [2/5] --sampling [random/smote/svmsmote/border/tomek] --random_state 99 --model [svm/rf/xgboost] --param1 [int] --param2 [int/str]
#


# [1] find optimal hyperparameters:
#
# 2-svm-hyperparameters
#classification/ml.py --in 2-all.pkl --out 2-hyper-svm --hyper --sampling random --random_state 99 --model svm 
# 2-rf-hyperparameters
#classification/ml.py --in 2-all.pkl --out 2-hyper-rf --hyper --sampling random --random_state 99 --model rf
# 2-xgboost-hyperparameters
#classification/ml.py --in 2-all.pkl --out 2-hyper-xgboost --hyper --sampling random --random_state 99 --model xgboost
#
# 5-svm-hyperparameters
#classification/ml.py --in 5-all.pkl --out 5-hyper-svm --hyper --sampling random --random_state 99 --model svm 
# 5-rf-hyperparameters
#classification/ml.py --in 5-all.pkl --out 5-hyper-rf --hyper --sampling random --random_state 99 --model rf
# 5-xgboost-hyperparameters
#classification/ml.py --in 5-all.pkl --out 5-hyper-xgboost --hyper --sampling random --random_state 99 --model xgboost



# [2] classification

# [svm]
# 2-all-svm
classification/ml.py --in 2-all.pkl --out 2-all-svm --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-10-svm
classification/ml.py --in 2-10.pkl --out 2-10-svm --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-20-svm
classification/ml.py --in 2-20.pkl --out 2-20-svm --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-30-svm
classification/ml.py --in 2-30.pkl --out 2-30-svm --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128

# [random-forest]
# 2-all-rf
classification/ml.py --in 2-all.pkl --out 2-all-rf --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-10-rf
classification/ml.py --in 2-10.pkl --out 2-10-rf --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-20-rf
classification/ml.py --in 2-20.pkl --out 2-20-rf --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-30-rf
classification/ml.py --in 2-30.pkl --out 2-30-rf --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini

# [xgboost]
# 2-all-xgboost
classification/ml.py --in 2-all.pkl --out 2-all-xgboost --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-10-xgboost
classification/ml.py --in 2-10.pkl --out 2-10-xgboost --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-20-xgboost
classification/ml.py --in 2-20.pkl --out 2-20-xgboost --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-30-xgboost
classification/ml.py --in 2-30.pkl --out 2-30-xgboost --label 2 --sampling random --random_state 99 --model xgboost --param1 20 

# [svm]
# 5-all-svm
classification/ml.py --in 5-all.pkl --out 5-all-svm --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-10-svm
classification/ml.py --in 5-10.pkl --out 5-10-svm --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-20-svm
classification/ml.py --in 5-20.pkl --out 5-20-svm --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-30-svm
classification/ml.py --in 5-30.pkl --out 5-30-svm --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128

# [random-forest]
# 5-all-rf
classification/ml.py --in 5-all.pkl --out 5-all-rf --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-10-rf
classification/ml.py --in 5-10.pkl --out 5-10-rf --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-20-rf
classification/ml.py --in 5-20.pkl --out 5-20-rf --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-30-rf
classification/ml.py --in 5-30.pkl --out 5-30-rf --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini

# [xgboost]
# 5-all-xgboost
classification/ml.py --in 5-all.pkl --out 5-all-xgboost --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-10-xgboost
classification/ml.py --in 5-10.pkl --out 5-10-xgboost --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-20-xgboost
classification/ml.py --in 5-20.pkl --out 5-20-xgboost --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-30-xgboost
classification/ml.py --in 5-30.pkl --out 5-30-xgboost --label 5 --sampling random --random_state 99 --model xgboost --param1 20 

