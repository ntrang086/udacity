#!/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""

from data import process_map
import json


def write_to_json(infile, json_file):
    data = process_map(infile)
    
    # write item by item
    with open(json_file, "w") as jf:
        for a in data:
            json.dump(a, jf, indent=2)
            jf.write("\n")

  
if __name__ == "__main__":
    json_file = "../chicago_small.json"

    # write data into a json file
    write_to_json('../chicago_small.osm', json_file)

    # count the number of items if having written item by item into the json file
    count = 0
    with open(json_file, "r") as f:
        for line in f:
            while True:
                try:
                    jfile = json.loads(line)
                    break
                except ValueError:
                    # Not yet a complete JSON value
                    line += next(f)
            count += 1
    print "number of json objects written to json file:", count