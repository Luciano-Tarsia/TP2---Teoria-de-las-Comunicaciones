#!/usr/bin/env python3

from statistics import mean
import sys
from scapy.all import *
from time import *
from pandas import DataFrame
import taller2_punto_opcional as po

SAVE_PATH = "./data/"

def most_frequent(List):
    return max(set(List), key = List.count)

dest_ip = sys.argv[1]

responses = {}
max_ttl = 30
max_tries = 30

print(f"Starting to traceroute IP {dest_ip}.")
print(f"Attempting to trace a route with a maximum of {max_ttl} steps.")

for ttl in range(1,max_ttl + 1):
    print(f"Starting with TTL number {ttl}.")
    for i in range(max_tries):
        print(f"TTL number {ttl}, packet number {i}.")
        probe = IP(dst=dest_ip, ttl=ttl) / ICMP()
        print("sending...")
        t_i = time()
        ans = sr1(probe, verbose=False, timeout=0.8)
        t_f = time()
        print("arrived")
        rtt = (t_f - t_i)*1000
        if ans is not None:
            if ttl not in responses:
                responses[ttl] = []
            responses[ttl].append((ans.src, rtt))
            print(responses[ttl])
print("Done with packets!")
#for ttl in responses:
#    print(ttl, responses[ttl]

results = []
for ttl in responses:
    print(f"Getting most frequent ip and mean rtt for jump number {ttl}.")
    responses_in_step = responses[ttl]
    
    ips = [response[0] for response in responses_in_step]
    most_frequent_ip = most_frequent(ips)
    
    # mean of rtts corresponding to most frequent ip
    rtts = [response[1] for response in responses_in_step if response[0] == most_frequent_ip]
    mean_rtt = sum(rtts)/len(rtts)
    
    print(f"{[ttl, most_frequent_ip, mean_rtt]}")
    results.append([ttl, most_frequent_ip, mean_rtt])

print("Calculating jumps between rtts.")

for i in range(1, len(results)):
    jump = results[i][2] - results[i-1][2]
    if jump < 0:
        j = 1
        while i - j > 0 and jump < 0:
            j += 1
            jump = results[i][2] - results[i-j][2]
    results[i][2] = max(jump, 0)

print("Done! Saving data in data/ folder.")

# so we don't overwrite
filename = SAVE_PATH + f"{dest_ip} " + strftime("%m-%d-%Y %H:%M:%S", localtime()) + ".csv"

df = DataFrame(results, columns = ["ttl", "ip", "rtt"])
df.to_csv(filename, index=False)

