#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import json
from pymongo import MongoClient


# sample: https://docs.google.com/document/d/1F0Vs14oNEs2idFJR3C_OPxwS6L0HPliOii-QpbmrMo4/pub

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm

    # Number of documents
    print "Number of documents", db.chicago.find().count()

    # Number of nodes
    print "Number of nodes", db.chicago.find({"type":"node"}).count()
                                                
    # Number of ways
    print "Number of ways", db.chicago.find({"type":"way"}).count()

    # Number of unique users -- wrong, need to fix
    #print "Number of unique users", db.chicago.distinct({"created.user"}).length
                                                    
    # Top 1 contributing user
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort": {"count": -1}}, {"$limit":1}]
    result = [doc for doc in db.chicago.aggregate(pipeline)]
    print "\nTop 1 contributing user", result

    # Number of users appearing only once (having 1 post)
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
    {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}]
    result = [doc for doc in db.chicago.aggregate(pipeline)]
    print "\nNumber of users appearing only once (having 1 post)", result
    # “_id” represents postcount


    # Top 10 appearing amenities
    pipeline = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity",
    "count":{"$sum":1}}}, {"$sort":{"count": -1}}, {"$limit":10}]
    result = [doc for doc in db.chicago.aggregate(pipeline)]
    print "\nTop 10 appearing amenities", result

    # Biggest religion (no surprise here)
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
    {"$group":{"_id":"$religion", "count":{"$sum":1}}},
    {"$sort":{"count": -1}}, {"$limit":1}]
    result = [doc for doc in db.chicago.aggregate(pipeline)]
    print "\nBiggest religion", result

    # Most popular cuisines
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}}, 
    {"$group":{"_id":"$cuisine", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":2}]
    result = [doc for doc in db.chicago.aggregate(pipeline)]
    print "\nMost popular cuisines", result