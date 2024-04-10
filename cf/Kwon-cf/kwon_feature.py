#!usr/bin/env python3

"""
<file>    kwon_feature.py
<brief>   kwon's CF feautre written by Huang.
"""

# constants
DIRECTION_IN = 1
DIRECTION_OUT = -1

# trace: [[time, direction], ...]
def kwon_feature(trace):
    # direction trace
    directions = [x[1] for x in trace]

    incoming_packets = directions.count(DIRECTION_IN)
    outgoing_packets = directions.count(DIRECTION_OUT)

    DoA = trace[-1][0] - trace[0][0]

    first_10_cell_sequence = directions[:9]

    first_50_in = directions[:50].count(DIRECTION_IN)
    first_50_out = directions[:50].count(DIRECTION_OUT)

    all_features = []
    # [1] number of incoming/outgoing packets
    #all_features.append(incoming_packets)
    #all_features.append(outgoing_packets)
    # [2] Duration of Activity
    #all_features.append(DoA)
    # [3] first 10 cell sequence
    all_features.extend(first_10_cell_sequence)
    # [4] fraction of incoming/outgoing cells of the frist 50 cells
    #all_features.append(first_50_in/50.0)
    #all_features.append(first_50_out/50.0)


    # when less than max_size, fill 0
    all_features.extend(0 for _ in range(15-len(all_features))) 
    

    return all_features[:15]


