#
# extract features from traces
#
#
# all parameters:
# extract.py --in <~/cf/dataset>  --out <~/cf/feature/*.pkl> --label 2/5 --length -1/10/20/30
#
#

# 2-all
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/2-all.pkl --label 2 --length -1
# 2-10
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/2-10.pkl --label 2 --length 10
# 2-20
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/2-20.pkl --label 2 --length 20
# 2-30
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/2-30.pkl --label 2 --length 30

# 5-all
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/5-all.pkl --label 5 --length -1
# 5-10
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/5-10.pkl --label 5 --length 10
# 5-20
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/5-20.pkl --label 5 --length 20
# 5-30
extract-feature/extract.py --in ~/desktop/cf/dataset --out ~/desktop/cf/feature/5-30.pkl --label 5 --length 30