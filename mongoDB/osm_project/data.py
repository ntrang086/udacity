#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict


OSMFILE = "../chicago_small.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


"""
Find out not only what tags are there, but also how many.
Return a dictionary with the tag name as the key and number of times this tag 
can be encountered in the map as value.
"""
def count_tags(filename):
    # YOUR CODE HERE
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag] += 1
            #print elem.tag, tags[elem.tag]
        else:
            tags[elem.tag] = 1
            #print elem.tag, tags[elem.tag]
    return tags


"""
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB, as well as
see if there are any other potential problems.
"""
def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        k = element.get("k")
        if lower.search(k):
            keys["lower"] += 1
        elif lower_colon.search(k):
            keys["lower_colon"] += 1
        elif problemchars.search(k):
            keys["problemchars"] += 1
            print k, element.attrib # "traffic control" has a whitespace
        else:
            keys["other"] += 1
            #print k
        
    return keys


"""
Find out how many unique users have contributed to the map in this particular area.
The function process_map should return a set of unique user IDs ("uid")
"""
def get_user(element):
    user = element.get("user")
    return user


"""
Improve street names in two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected_st_type = ["Street", "Avenue", "Boulevard", "Circle", "Commons", "Court", "Drive", "Highway", "Lane", "Park", "Parkway", "Place", "Road", 
            "Square", "Terrace", "Trail", "Way"]

mapping_st_type = { "St": "Street",
            "St.": "Street",
            "St": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "AVE": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "CT": "Court",
            "Ct": "Court",
            "Cir": "Circle",
            "Dr": "Drive",
            "LN": "Lane",
            "Ln": "Lane",
            "PKWY": "Parkway",
            "Pkwy": "Parkway",
            "Rd": "Road",
            "Trl": "Trail",
            # Special cases
            "Damen": "Damen Street", # 'Damen': set(['N Damen']),
            "Broadway": "Broadway Street" # 'Blvd': set(['Sauk Blvd'])
            } 


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_st_type:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    
    return street_types


def update_name(name, mapping):
    st = street_type_re.search(name)
    if st:
        st_type = st.group()
        if st_type in mapping:
            name = name[:-len(st_type)] + mapping[st_type]

    return name



"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag
        node["created"] = {}
        if element.get("id") != None: 
            node["id"] = element.get("id")
        if element.get("visible") != None: 
            node["visible"] = element.get("visible")
        for entry in CREATED:
            if element.get(entry):
                node["created"][entry] = element.get(entry)
        if element.get("lat") and element.get("lon"):
            node["pos"] = [float(element.get("lat")), float(element.get("lon"))]
        
        # initialize these temporary dictionary and list; if they are not empty, then append them to the node dictionary
        address_dict = {}
        node_refs = []

        # iterate through the children of elements "node" and "way" and look for "tag" and "nd"
        for child in element.iter():
            if child.tag == "tag":
                key = child.attrib["k"]
                value = child.attrib["v"]
                if problemchars.search(key):
                    continue
                elif key.startswith("addr:") and key.count(":") == 1: # ignore address with the 2nd ":"
                    better_name = update_name(value, mapping_st_type)
                    address_dict[key.split(":")[1]] = better_name
                elif not key.startswith("addr:"):
                    node[key] = value
            elif child.tag == "nd":
                node_refs.append(child.attrib["ref"])
                node["node_refs"] = node_refs

        # if address_dict is not empty, set it to node["address"] 
        if address_dict != {}:
            node["address"] = address_dict

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data



# Below are test functions for the above functions

def test_count_tags():
    tags = count_tags(OSMFILE)
    pprint.pprint(tags)


def test_key_type():
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(OSMFILE):
        keys = key_type(element, keys)    
    pprint.pprint(keys)


def test_get_user():
    users = set()
    for _, element in ET.iterparse(OSMFILE):
        user = get_user(element)
        if user != None:
            users.add(user)
    pprint.pprint(users)
    print "total number of users:", len(users)


def test_street_type():
    st_types = audit(OSMFILE)
    print len(st_types)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_st_type)
            print name, "=>", better_name



def test_process():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map(OSMFILE)
    
    for entry in data: # print only entries with an address
        if "address" in entry:
            pprint.pprint(entry)


if __name__ == "__main__":
    #test_count_tags()
    #test_key_type()
    #test_get_user()
    #test_street_type()
    test_process()