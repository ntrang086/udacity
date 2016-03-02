#!/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""

from autos import process_file


def insert_autos(infile, db):
    data = process_file(infile)
    
    # Add your code here. Insert the data in one command.
    db.autos.insert(data)
    
    
  
if __name__ == "__main__":
    # Code here is for local use on your own computer.
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    # check the number of autos before and after insert
    num_autos = db.autos.find().count()
    print "num_autos before:", num_autos

    # insert data into the database. Make sure to run only once
    insert_autos('../autos.csv', db)

    num_autos = db.autos.find().count()
    print "num_autos after:", num_autos
    print db.autos.find_one()
    
    # print everything in autos. comment out insert_autos before running this; you wouldn't want to insert data more than once
    #for a in db.autos.find():
     #   print a

    # remove everything from autos collection
    #print db.autos.remove()