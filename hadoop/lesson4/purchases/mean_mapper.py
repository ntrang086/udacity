#!/usr/bin/python

# Mapper code to produce the sale for each weekday. This will be used to find the mean sale for a day

import sys
from datetime import datetime

for line in sys.stdin:
    data = line.strip().split('\t')
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
        print "{0}\t{1}".format(weekday, cost)


          
"""
def main():
    mapper()


if __name__ == "__main__":
    main()

"""