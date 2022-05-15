#!/usr/bin/env python3

import sys
from scapy.all import *
from time import *

def most_frequent(List):
    return max(set(List), key = List.count)

responses = {}
for i in range(10):
    for ttl in range(1,25):
        probe = IP(dst=sys.argv[1], ttl=ttl) / ICMP()
        t_i = time()
        ans = sr1(probe, verbose=False, timeout=0.8)
        t_f = time()
        rtt = (t_f - t_i)*1000
        if ans is not None:
            if ttl not in responses:
                responses[ttl] = []
            responses[ttl].append((ans.src, rtt))

#for ttl in responses:
#    print(ttl, responses[ttl])

for ttl in responses:
    rtts = []
    ips = []
    for jump in responses[ttl]:
        ips.append(jump[0])
        rtts.append(jump[1])

    mean_rtt = sum(rtts)/len(rtts)
    most_frequent_ip = most_frequent(ips)

    print(ttl, most_frequent_ip, mean_rtt)