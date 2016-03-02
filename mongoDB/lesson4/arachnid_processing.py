#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
  * Note that the value associated with the classification key is a dictionary with
    taxonomic labels.
"""

import codecs
import csv
import json
import pprint
import re

DATAFILE = '../arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def strip_spider(v):
    return re.sub(r"\s\(spider\)\s*", " ", v) # in some URIs, there is (spider), so only remove (spider) with ONE leading space char
    """
    \s is whitespace
    * Causes the resulting RE to match 0 or more repetitions of the preceding RE, as many repetitions 
    as are possible. ab* will match ‘a’, ‘ab’, or ‘a’ followed by any number of ‘b’s.
    """

    
# Trang updated to check for Null values
def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    elif v == "NULL":
        return None    
    return v


# Trang updated to check for Null values; this function creates a list as long as synonym has one non-NULL value
# Also added a line to strip * 
def parse_array_synonym(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip("*") for i in v_array]
        v_array = [i.strip() for i in v_array]
        return v_array
    elif v == "NULL":
        return None
    return [v]

    
def process_file(filename):

    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            # YOUR CODE HERE
            arachnid = {}
            classification = {}
            for field, val in line.iteritems():
                if field not in FIELDS:
                    continue
                val = strip_spider(val)
                val = val.strip()
                if field == "name":
                    if not line[field].isalnum() or line[field] == "NULL":
                        arachnid[FIELDS[field]] = line['rdf-schema#label']
                    else:
                        arachnid[FIELDS[field]] = val
                elif field == "synonym":
                    val = parse_array_synonym(val)
                    arachnid[FIELDS[field]] = val
                elif field in ['family_label','class_label', 'phylum_label', 'order_label', 'kingdom_label', 'genus_label']:
                    val = parse_array(val)
                    classification[FIELDS[field]] = val
                else:
                    arachnid[FIELDS[field]] = val
            if classification:
                arachnid["classification"] = classification
            data.append(arachnid)
    return data


# Trang added Original Fields and audit_file to audit Arachnid.csv file
ORIGINAL_FIELDS = ['rdf-schema#label', 'URI', 'rdf-schema#comment', 'synonym', 'name', 'family_label',
                   'class_label', 'phylum_label', 'order_label', 'kingdom_label', 'genus_label']


def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        # initialize the fields:
        for field in fields:
            fieldtypes[field] = set()        
        for line in reader:
            if not line["URI"].startswith("http://dbpedia.org/"):
                continue
            for field in fields:
                try:
                    if line[field] == "NULL" or line[field] == "":
                        fieldtypes[field].add(type(None))
                    elif line[field].startswith("{"):
                        fieldtypes[field].add(type([]))
                        #if field == 'synonym':
                         #   print line[field]
                    elif int(line[field]):
                        fieldtypes[field].add(type(1))
                    elif float(line[field]):
                        fieldtypes[field].add(type(1.0))
                except ValueError:
                    try:
                        if float(line[field]):
                            fieldtypes[field].add(type(1.0))
                    except ValueError:
                        fieldtypes[field].add(type(""))
                        #if field == 'rdf-schema#label':
                         #   print line[field]
    return fieldtypes


def test_audit():
    fieldtypes = audit_file(DATAFILE, ORIGINAL_FIELDS)
    pprint.pprint(fieldtypes)

    

def test():
    #print "Test audit function:"
    #test_audit()
    data = process_file(DATAFILE)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None, 
        "name": "Argiope", 
        "classification": {
            "kingdom": "Animal", 
            "family": "Orb-weaver spider", 
            "order": "Spider", 
            "phylum": "Arthropod", 
            "genus": None, 
            "class": "Arachnid"
        }, 
        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
        "label": "Argiope", 
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }


    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]
    # Trang added below 2 assertations
    assert data[57]["label"] == "Hottentotta tamulus"
    assert data[57]["synonym"] == ["H. tamulus concanensis (Pocock 1900)", "H. tamulus gangeticus (Pocock 1900)", "H. tamulus gujaratensis (Pocock 1900)", "H. tamulus sindicus (Pocock 1900)"]

if __name__ == "__main__":
    test()
    
    
"""
Results of auditing the file:
{'URI': set([<type 'str'>]),
 'class_label': set([<type 'list'>, <type 'str'>]),
 'family_label': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]),
 'genus_label': set([<type 'NoneType'>, <type 'str'>]),
 'kingdom_label': set([<type 'list'>, <type 'str'>]),
 'name': set([<type 'NoneType'>, <type 'str'>]),
 'order_label': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]),
 'phylum_label': set([<type 'list'>, <type 'str'>]),
 'rdf-schema#comment': set([<type 'str'>]),
 'rdf-schema#label': set([<type 'str'>]),
 'synonym': set([<type 'NoneType'>, <type 'list'>, <type 'str'>])}
"""