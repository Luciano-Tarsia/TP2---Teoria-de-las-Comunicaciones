#!/usr/bin/env python3

import sys
from scapy.all import *
from time import *
from pandas import DataFrame

SAVE_PATH = "./data/"

dest_ip = sys.argv[1]

responses = {}
max_ttl = 30
max_tries = 30

print(f"Starting to traceroute IP {dest_ip}.")
print(f"Attempting to trace a route with a maximum of {max_ttl} steps.")

for ttl in range(1, max_ttl + 1):
    print(f"Starting with TTL number {ttl}.")
    for i in range(1, max_tries + 1):
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

results = []
for ttl, ans in responses.items():
    for ip, rtt in ans:
        results.append([ttl, ip, rtt])
print(results)


print("Done! Saving data in data/ folder.")

# so we don't overwrite
filename = SAVE_PATH + f"{dest_ip} (all ips) " + strftime("%m-%d-%Y %H:%M:%S", localtime()) + ".csv"

df = DataFrame(results, columns = ["ttl", "ip", "rtt"])
df.to_csv(filename, index=False)

