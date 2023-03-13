#!usr/bin/env python3

"""
<file>    kwon_feature.py
<brief>   kwon's WF feautres.
"""

max_count = 100

#time and direction
def kwon_feature(times, dirs):

    features = []

    size = len(times)

    features.append(size) #num packets
    features.append(len([d for d in dirs if d > 0])) #num outgoing
    features.append(len([d for d in dirs if d < 0])) #num incoming
    features.append(times[-1] - times[0]) #transmission time

    #locations of outgoing packets
    count = 0
    for i in range(0, size):
        if dirs[i] > 0:
            features.append(i)
            count += 1
        if count >= max_count:
            break
    for i in range(count, max_count):
        features.append(-1)

    #burst of incoming packets
    count = 0
    prevloc = 0
    for i in range(0, len(dirs)):
        if dirs[i] > 0:
            count += 1
            features.append(i - prevloc)
            prevloc = i
        if count == max_count:
            break
    for i in range(count, max_count):
        features.append(-1)

    #burst of outgoing packets
    bursts = []
    curburst = 0
    stopped = 0
    for x in dirs:
        if x < 0:
            stopped = 0
            curburst -= x
        if x > 0 and stopped == 0:
            stopped = 1
        if x > 0 and stopped == 1:
            stopped = 0
            bursts.append(curburst)
    features.append(max(bursts))
    features.append(sum(bursts)/len(bursts))
    features.append(len(bursts))
    counts = [0, 0, 0]
    for x in bursts:
        if x > 5:
            counts[0] += 1
        if x > 10:
            counts[1] += 1
        if x > 15:
            counts[2] += 1
    features.append(counts[0])
    features.append(counts[1])
    features.append(counts[2])

    return features

