#!/bin/bash


infile=data

outfile=5-all


echo "---------------     run Huang's CF     ---------------"
./run_CF.py --in $infile --out $outfile

echo "----------  all done   ----------"


