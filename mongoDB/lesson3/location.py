#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

If you look at the full city data, you will notice that there are couple of values that seem to provide
the same information in different formats: "point" seems to be the combination of "wgs84_pos#lat" and "wgs84_pos#long".
However we do not know if that is the case and should check if they are equivalent.

Finish the function check_loc(). It will receive 3 strings, first will be the combined value of "point" and then the
"wgs84_pos#" values separately. You have to extract the lat and long values from the "point" and compare
to the "wgs84_pos# values and return True or False.

Note that you do not have to fix the values, just determine if they are consistent. To fix them in this case
you would need more information. Feel free to discuss possible strategies for fixing this on the discussion forum.

The rest of the code is just an example on how this function can be used.
Changes to "process_file" function will not be take into account.
"""
import csv
import pprint

CITIES = '../cities_udacity.csv'

def findOccurences(string, character): # helper function to find a separator in a list
    occurences = []
    for i, letter in enumerate(string):
        if letter == character:
            occurences.append(i)
    return occurences


def convert_str_to_list(string, start_char="", end_char="", separator=""): # works for string with that start with a bracket or other chars, e.g. {abc|def}
    separator_pos = findOccurences(string, separator)
    current_pos = 0
    if start_char != "":
        current_pos = 1 # skip the start char, e.g. "{"
    i = 0
    temp = []
    while i < len(separator_pos):
        temp.append(string[current_pos:separator_pos[i]])
        current_pos += separator_pos[i]
        i += 1
    if end_char != "":
        temp.append(string[current_pos:len(string)-1]) # add the last string, skip the end char, e.g.  "}"
    else:
        temp.append(string[current_pos+1:len(string)]) # add the last string
    return temp


def compare_list(a, b): # check if at least 1 element in a is in b
    for i in a:
        if i in b:
            return True
    return False


def check_loc(point, lat, longi):
    # YOUR CODE HERE

    # from audit.py: 'point': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]); not actual str type, but a combination of lat & long separated by " "
    # from audit.py: 'wgs84_pos#lat': set([<type 'NoneType'>, <type 'list'>, <type 'float'>])
    # from audit.py: 'wgs84_pos#long': set([<type 'NoneType'>, <type 'list'>, <type 'float'>])
    # special case: point {26.92 80.72|26.94 80.72} lat {26.92|26.94} long 80.72
    # special case: point {20.52 76.12|20.535997 76.112408} lat {20.52|20.536} long {76.1124|76.12}
    # special case: point {25.21 85.02|25.35 85.03333333333333} lat {25.21|25.35} long {85.02|85.0333}  no rounding up; should be False in this case
    
    point_list = []
    lat_in_point = [] # lat value in point
    longi_in_point = [] # longi value in point

    lat_list = []
    longi_list = []
    if (point == "NULL" and lat == "NULL" and longi == "NULL") or (point == "" and lat == "" and longi == ""):
        return True
    
    # convert point to list
    if point.startswith("{"):        
        point_list = convert_str_to_list(point, "{", "}", "|")
    else:
        point_list = [point]
    
    # add lat from point_list to lat_in_point and longi from point_list to longi_in_point
    for entry in point_list:
        temp = convert_str_to_list(entry, separator=" ")
        if temp[0] not in lat_in_point:
            lat_in_point.append(temp[0])
        if temp[1] not in longi_in_point:
            longi_in_point.append(temp[1])

    # convert lat to list
    if lat.startswith("{"):        
        lat_list = convert_str_to_list(lat, "{", "}", "|")
    else:
        lat_list = [lat]
    
    # convert longi to list
    if longi.startswith("{"):        
        longi_list = convert_str_to_list(lat, "{", "}", "|")
    else:
        longi_list = [longi]

    return (compare_list(lat_in_point, lat_list) and compare_list(longi_in_point, longi_list))

    

def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra matadata
        for i in range(3):
            l = reader.next()
        # processing file
        for line in reader:
            # calling your function to check the location
            result = check_loc(line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            if not result:
                print "{}: {} != {} {}".format(line["name"], line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            data.append(line)

    return data



def test():
    assert check_loc("33.08 75.28", "33.08", "75.28") == True
    assert check_loc("44.57833333333333 -91.21833333333333", "44.5783", "-91.2183") == False

if __name__ == "__main__":
    test()