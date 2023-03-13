#!/bin/bash

# trace directory
data=client
# feature pickle file
feature=feature.pkl
# classication results
result=client-rf


echo "--------  run Huang's WF --------"
  
  #./extract.py --in $data
  ./classify.py --in $data/$feature --out $result

echo "----------  all done   ----------"

#for i in {1..10}
#do
#  echo "---------------     run for the $i time    ---------------"
#  ./classify.py --in $data/$feature --out $result-$i

#done

