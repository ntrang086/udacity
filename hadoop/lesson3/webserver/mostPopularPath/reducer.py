#!/usr/bin/python


# Reducer code to produce the file whose path occurs most often in access_log


import sys

count = 0
oldKey = None
highest_count = 0
most_popular_path = ""

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisSize = data_mapped

    if oldKey and oldKey != thisKey:
        # Keep track of highest_count and most_popular_path
        if highest_count < count:
            highest_count = count
            most_popular_path = oldKey
        # Move on to the next key
        oldKey = thisKey;
        count = 0

    oldKey = thisKey
    count = count + 1
# See if the last key is the most popular path
if highest_count < count:
    highest_count = count
    most_popular_path = oldKey
print most_popular_path, "\t", highest_count

