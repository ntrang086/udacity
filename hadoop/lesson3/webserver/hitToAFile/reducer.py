#!/usr/bin/python

# Reducer code to display the number of hits for each different file on the website 

import sys

count = 0
url = "/assets/js/the-associates.js"


for line in sys.stdin:
    data_mapped = line.strip().split()
    if len(data_mapped) != 1:
        # Something has gone wrong. Skip this line.
        continue

    thisKey = data_mapped[0]

    if thisKey == url:
        count += 1
print count
