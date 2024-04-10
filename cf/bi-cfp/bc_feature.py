#!/usr/bin/env python3

"""
<file>    bc_feature.py
<brief>   feature vectors for XX model
"""

import itertools
import numpy as np

OUT = 1
IN = -1

def get_feature(trace, max_size=5000):
    all_feature = []

    # [1] number of RELAY_EARLY cells
    all_feature.append(num_relay_early(trace))
    all_feature.extend(cell_count(trace))
    all_feature.extend(equal_width_sequ(trace))
    all_feature.extend(burst_sequ(trace))

    return all_feature

def num_relay_early(trace):
    cell_types = [x[0] for x in trace]

    RELAY_EARLY = 9
    count_of_re = cell_types.count(RELAY_EARLY)

    return count_of_re

def cell_count(trace):
    directions = [x[1] for x in trace]

    total = len(directions)
    total_in = len([x for x in directions if x < 0])
    total_out = len([x for x in directions if x > 0])

    first_20_out = len([x for x in directions[:20] if x > 0])
    first_30_out = len([x for x in directions[:30] if x > 0])

    return [total, total_out, total_in, total_out/float(total), first_20_out, first_30_out]

def equal_width_sequ(trace):
    directions = [x[1] for x in trace]

    chunks = [directions[i:i+10] for i in range(0, len(directions), 10)]
    chunk_out = [ch.count(OUT) for ch in chunks]

    return [np.mean(chunk_out), np.std(chunk_out), min(chunk_out), max(chunk_out)]

def burst_sequ(trace):
    directions = [x[1] for x in trace]

    burst = [k*len(list(v)) for k,v in itertools.groupby(directions)]
    burst_out = [b for b in burst if b > 0]
    burst_in = [b for b in burst if b < 0]

    return [min(burst), max(burst), len(burst), len(burst_out), len(burst_in), len(burst_out)/float(len(burst)), len(burst_in)/float(len(burst)), np.mean(burst), np.std(burst)]


