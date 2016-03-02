#!/usr/bin/python


"""
The data set we're using is an anonymized Web server log file from a public relations company whose clients were DVD distributors. 
The log file is in the udacity_training/data directory, and it's currently compressed using GnuZip. 
So you'll need to decompress it and then put it in HDFS. If you take a look at the file, 
you'll see that each line represents a hit to the Web server. It includes the IP address which accessed the site, 
the date and time of the access, and the name of the page which was visited.
"""

# Mapper code to export all the hits to the web server

import sys

for line in sys.stdin:
    data = line.strip().split(" ")
    if len(data) == 10:
        ip, client_id, user, time, zone, method, path, protocol, status, size = data
        print "{0}".format(path)

