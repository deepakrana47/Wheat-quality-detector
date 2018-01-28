import numpy as np
def areaThreshold_by_avg(axis, exp):
    avga = np.average([(s[1] - s[0]) * (s[3] - s[2]) for i,s in axis.items()])
    low = avga/2**exp
    high = avga*2**exp
    return low, high

def areaThreshold_by_havg(axis, exp):
    areas = np.sort([(s[1] - s[0]) * (s[3] - s[2]) for i,s in axis.items()])
    alen = len(areas)
    avga = np.average([areas[i] for i in range(alen/2**exp, int(alen*(1-1.0/2**exp)))])
    low = avga / 2 ** exp
    high = avga * 2 ** exp
    return low, high