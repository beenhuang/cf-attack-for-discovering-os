#!/bin/bash

# trace directory
data=data
# feature pickle file
feature=feature.pkl
# classication results
result=Kwon-c45


echo "--------  run Kwon's CF --------"
  
  ./extract.py --in $data
  ./classify.py --in $feature --out $result

echo "----------  all done   ----------"
