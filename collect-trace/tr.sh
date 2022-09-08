#
# extract traces from logs
#
#
# all parameters:
# trace.py --in <~/dataset>  --out <~/feature/*.pkl> --label [2/5] --length []-1/10/20/30]
#
#

# general mode
collect-trace/trace.py --in "tornet0.01(seed=1)"  --out "general(s1).csv"  --mode general

# hs mode
collect-trace/trace.py --in "tornet0.01-hs(seed=1)"  --out "hs(s1).csv"  --mode hs
