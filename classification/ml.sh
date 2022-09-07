#
# classification
#
#
# [1] find optimal hyperparameters:
# ml.py --in <~/cf/feature/*.pkl>  --out <~/cf/results/hyperparameters/*.txt> --hyper --sampling [random/smote/svmsmote/border/tomek] --random_state 99 --model [svm/rf/xgboost]
#
# [2] classification
# ml.py --in <~/cf/feature/*.pkl>  --out <~/cf/results/*.txt> --label [2/5] --sampling [random/smote/svmsmote/border/tomek] --random_state 99 --model [svm/rf/xgboost] --param1 [int] --param2 [int/str]
#


# [1] find optimal hyperparameters:

# 2-svm-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/hyperparameters/2-svm-hyper.txt --hyper --sampling random --random_state 99 --model svm 
# 2-rf-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/hyperparameters/2-rf-hyper.txt --hyper --sampling random --random_state 99 --model rf
# 2-xgboost-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/hyperparameters/2-xgboost-hyper.txt --hyper --sampling random --random_state 99 --model xgboost

# 5-svm-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/hyperparameters/5-svm-hyper.txt --hyper --sampling random --random_state 99 --model svm 
# 5-rf-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/hyperparameters/5-rf-hyper.txt --hyper --sampling random --random_state 99 --model rf
# 5-xgboost-hyperparameters
#machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/hyperparameters/5-xgboost-hyper.txt --hyper --sampling random --random_state 99 --model xgboost


# [2] classification

# [svm]
# 2-all-svm
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/2-all-svm.txt --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-10-svm
#machine-learning/ml.py --in ~/desktop/cf/feature/2-10.pkl --out ~/desktop/cf/results/2-10-svm.txt --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-20-svm
#machine-learning/ml.py --in ~/desktop/cf/feature/2-20.pkl --out ~/desktop/cf/results/2-20-svm.txt --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128
# 2-30-svm
#machine-learning/ml.py --in ~/desktop/cf/feature/2-30.pkl --out ~/desktop/cf/results/2-30-svm.txt --label 2 --sampling random --random_state 99 --model svm --param1 128 --param2 128

# [random-forest]
# 2-all-rf
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/2-all-rf.txt --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-10-rf
#machine-learning/ml.py --in ~/desktop/cf/feature/2-10.pkl --out ~/desktop/cf/results/2-10-rf.txt --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-20-rf
#machine-learning/ml.py --in ~/desktop/cf/feature/2-20.pkl --out ~/desktop/cf/results/2-20-rf.txt --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 2-30-rf
#machine-learning/ml.py --in ~/desktop/cf/feature/2-30.pkl --out ~/desktop/cf/results/2-30-rf.txt --label 2 --sampling random --random_state 99 --model rf --param1 30 --param2 gini

# [xgboost]
# 2-all-xgboost
#machine-learning/ml.py --in ~/desktop/cf/feature/2-all.pkl --out ~/desktop/cf/results/2-all-xgboost.txt --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-10-xgboost
#machine-learning/ml.py --in ~/desktop/cf/feature/2-10.pkl --out ~/desktop/cf/results/2-10-xgboost.txt --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-20-xgboost
#machine-learning/ml.py --in ~/desktop/cf/feature/2-20.pkl --out ~/desktop/cf/results/2-20-xgboost.txt --label 2 --sampling random --random_state 99 --model xgboost --param1 20 
# 2-30-xgboost
#machine-learning/ml.py --in ~/desktop/cf/feature/2-30.pkl --out ~/desktop/cf/results/2-30-xgboost.txt --label 2 --sampling random --random_state 99 --model xgboost --param1 20 

# [svm]
# 5-all-svm
machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/5-all-svm.txt --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-10-svm
machine-learning/ml.py --in ~/desktop/cf/feature/5-10.pkl --out ~/desktop/cf/results/5-10-svm.txt --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-20-svm
machine-learning/ml.py --in ~/desktop/cf/feature/5-20.pkl --out ~/desktop/cf/results/5-20-svm.txt --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128
# 5-30-svm
machine-learning/ml.py --in ~/desktop/cf/feature/5-30.pkl --out ~/desktop/cf/results/5-30-svm.txt --label 5 --sampling random --random_state 99 --model svm --param1 512 --param2 128

# [random-forest]
# 5-all-rf
machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/5-all-rf.txt --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-10-rf
machine-learning/ml.py --in ~/desktop/cf/feature/5-10.pkl --out ~/desktop/cf/results/5-10-rf.txt --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-20-rf
machine-learning/ml.py --in ~/desktop/cf/feature/5-20.pkl --out ~/desktop/cf/results/5-20-rf.txt --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini
# 5-30-rf
machine-learning/ml.py --in ~/desktop/cf/feature/5-30.pkl --out ~/desktop/cf/results/5-30-rf.txt --label 5 --sampling random --random_state 99 --model rf --param1 30 --param2 gini

# [xgboost]
# 5-all-xgboost
machine-learning/ml.py --in ~/desktop/cf/feature/5-all.pkl --out ~/desktop/cf/results/5-all-xgboost.txt --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-10-xgboost
machine-learning/ml.py --in ~/desktop/cf/feature/5-10.pkl --out ~/desktop/cf/results/5-10-xgboost.txt --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-20-xgboost
machine-learning/ml.py --in ~/desktop/cf/feature/5-20.pkl --out ~/desktop/cf/results/5-20-xgboost.txt --label 5 --sampling random --random_state 99 --model xgboost --param1 20 
# 5-30-xgboost
machine-learning/ml.py --in ~/desktop/cf/feature/5-30.pkl --out ~/desktop/cf/results/5-30-xgboost.txt --label 5 --sampling random --random_state 99 --model xgboost --param1 20 

