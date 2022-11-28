#!/bin/bash


datadir=data

outfile=kwon


echo "---------------     run Kwon's CF     ---------------"
./run_CF.py --in $datadir --out $outfile

echo "----------  all done   ----------"


