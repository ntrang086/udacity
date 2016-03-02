#!/usr/bin/python

# Find the total sales of all stores

import sys

salesTotal = 0
numTotal = 0
key = None



for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisSale = data_mapped
    salesTotal += float(thisSale)
    numTotal += 1

print  salesTotal, "\t", numTotal

