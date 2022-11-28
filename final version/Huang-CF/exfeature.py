#!usr/bin/env python3

"""
<file>    exfeature.py
<brief>   extract features from a trace.
"""

from os.path import abspath, dirname, join, basename

# constants
DIRECTION_IN = 1
DIRECTION_OUT = -1


###########  get general trce  ##########

# general trace: [[timestamp1, direction1], [ts2, direct2], ... ]
def get_general_trace(trace):   
    if(trace[3] == 'general'):
        label = 0
    elif(trace[3] == 'IpClient'):
        label = 1
    elif(trace[3] == 'IpHS'):
        label = 2
    elif(trace[3] == 'RpClient'):
        label = 3
    elif(trace[3] == 'RpHS'):
        label = 4        

    return trace[4:], label


################## transform trace ###################

# get general in/out trace
def transform_general_inout_trace(trace):
    gen_in=[x for x in trace if int(x.split(":")[2]) == DIRECTION_IN]
    gen_out=[x for x in trace if int(x.split(":")[2]) == DIRECTION_OUT]

    return gen_in, gen_out


############# main function #################

def extract_features(trace):
    gen_total, label = get_general_trace(trace)
    gen_in, gen_out =  transform_general_inout_trace(gen_total) 

    all_features = []
    # [1] number of packets
    all_features.append(len(gen_total))
    # [2] number of outgoing packets
    all_features.append(len(gen_out))
    # [3] number of incoming packets
    all_features.append(len(gen_in))
    # [4] outgoing / total 
    all_features.append(len(gen_out)/float(len(gen_total)))
    # [5] incoming / total
    all_features.append(len(gen_in)/float(len(gen_total)))
 

    return all_features, label


if __name__ == "__main__":
    BASE_DIR = abspath(dirname(__file__))
    INPUT_DIR = join(BASE_DIR, "client")
    FILE_NAME = "6-33"

    features, label = extract_features(join(INPUT_DIR, FILE_NAME))

    #label = get_trace_label(join(INPUT_DIR, FILE_NAME))
    #print(f"label: {label}")

    print(f"[new] {FILE_NAME}, {len(features)}: ")
    for elem in features:
        print(elem) 

