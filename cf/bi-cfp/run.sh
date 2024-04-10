#!/bin/bash


# data directory
d_dir=data
res_dir=res
class=5


echo "--------  run Bi-CFP --------"
  ./extract.py --in $d_dir
  ./classify.py --out $res_dir --class $class
echo "----------  all done   ----------"
