#!/usr/bin/python

import sys

saleTotal = 0
oldKey = None

# Loop around the data
# It will be in the format key\tval
# Where key is the weekday, val is the sale amount
#
# All the sales for a particular key will be presented,
# then the key will change and we'll be dealing with the next one
# Goal: finding the sum of sale for each each weekday

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisSale = data_mapped

    if oldKey and oldKey != thisKey:
        print oldKey, "\t", saleTotal
        oldKey = thisKey;
        saleTotal = 0

    oldKey = thisKey
    saleTotal += float(thisSale)

if oldKey != None:
    print oldKey, "\t", saleTotal

