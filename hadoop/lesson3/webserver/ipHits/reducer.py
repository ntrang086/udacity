#!/usr/bin/python

# Reducer code to count the number of hits to the site made by each different IP address


import sys

count = 0
oldKey = None


for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisSize = data_mapped

    if oldKey and oldKey != thisKey:
        print oldKey, "\t", count
        oldKey = thisKey;
        count = 0

    oldKey = thisKey
    count = float(count) + 1

if oldKey != None:
    print oldKey, "\t", count

