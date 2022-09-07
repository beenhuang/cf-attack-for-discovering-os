#!/usr/bin/env python3

import argparse
import os
import sys
import pickle
import csv
import numpy as np

# argument parser:
parser = argparse.ArgumentParser()

# 1. input: 
parser.add_argument("--in", required=True, help="input dataset")

# 2. output: 
parser.add_argument("--out", required=True, help="output pickle file")

# 3. label: 
parser.add_argument("--label", required=False, type=int, 
                    default=2, help="label")

# 4. max length: the max length of cells.
parser.add_argument("--length", required=False, type=int, 
                    default=-1, help="max length of extracted cells")

args = vars(parser.parse_args())


#    
def get_files(dir):

    # get trace files
    files = []
    
    # 1. get general files:
    #
    g_dir = os.path.join(dir, 'general-trace') 

    # add g_file
    for file in os.listdir(g_dir): 
        g_file = os.path.join(g_dir, file)
        
        if os.path.splitext(g_file)[1] == '.csv':
            files.append(g_file)

    # 2. get hs files:
    #
    hs_dir = os.path.join(dir, 'hs-trace')

    # add hs_file
    for file in os.listdir(hs_dir): 
        hs_file = os.path.join(hs_dir, file)
        
        if os.path.splitext(hs_file)[1] == '.csv':
            files.append(hs_file) 

    return files

#                   
def get_one_trace_features(tag, trace, label):
    total = len(trace) # the total number of packets.
    outgoing = 0 # the number of outgoing packets.
    incoming = 0 # the number of incoming packets.
    oft = 0.0 # outgoing / total
    ift = 0.0 # incoming / total
    
    for cell in trace:
        ele = cell.split(':')
        
        # item[0] is cell command, item[1] is RELAY command, and item[2] is direction.
        if int(ele[2]) == -1: # outgoing packet
            outgoing += 1
        else : # incoming packet
            incoming += 1
            
    oft = outgoing / total
    ift = incoming / total
    
    if label == 2 :
        # client is 0, and onion service is 1.
        if(tag == 'general' or tag == 'IpClient' or tag == 'RpClient'):
            tagNum = 0
        else:
            tagNum = 1

    elif label == 5 :        
        if(tag == 'general'):
            tagNum = 0
        elif(tag == 'IpClient'):
            tagNum = 1
        elif(tag == 'IpHS'):
            tagNum = 3
        elif(tag == 'RpClient'):
            tagNum = 2
        elif(tag == 'RpHS'):
            tagNum = 4        
    

    row = [total, outgoing, incoming, oft, ift]

    return row, tagNum

#
def extract_features(files, label, length):

    # check label value :
    if label != 2 and label != 5 :
        print(f"[ERROR] invalid label : [{args['label']}]")
        sys.exit()

    # check maximum number
    max = length + 4    

    # data list
    data = []
    # target list
    target = []
    
    for file in files: # each file
        with open(file,'r') as f:
            row = csv.reader(f, delimiter=',')
            
            # travel element
            # row[0] : client_ID, row[1] : relay_ID, row[2] : circ_ID, row[3] : tag, row[4:] : trace
            for element in row:
                if length == -1 :
                    d, t = get_one_trace_features(element[3], element[4:], label)
                else :
                    d, t = get_one_trace_features(element[3], element[4:max], label)

                data.append(d)
                target.append(t)    

    #print(data)
    #print(target)
    
    return np.array(data, dtype=np.float64), np.array(target, dtype=int)
                

def main():
    print(f"-------  [extract.py]: start to run [{args['in']}]  -------")
    
    # [1] get all trace files
    files = get_files(args["in"])

    print(f"[LOAD] files, the length of files: [{len(files)}]")
    

    # [2] extract features
    data, target = extract_features(files, args["label"], args["length"])

    print(f"[GET] data&target, data length: [{len(data)}] ")


    # [3] dump data&target to pickle file
    with open(args["out"], "wb") as f:
        pickle.dump((data, target), f)

        print(f"[SAVED] data&target to the [{args['out']}] file") 

    print(f"-------  [extract.py]: completed successfully  -------")


if __name__ == "__main__":
    main()

