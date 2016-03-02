#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

print "number of people (data points):", len(enron_data)
print enron_data

count_poi = 0
count_salary = 0
count_email = 0
count_NaN_payments = 0
print "number of features per person:", len(enron_data['METTS MARK'])
for person in enron_data:
	if enron_data[person]['poi'] == True:
		count_poi += 1
	if enron_data[person]['salary'] != 'NaN':
		count_salary += 1
	if enron_data[person]['email_address'] != 'NaN':
		count_email += 1
	if enron_data[person]['total_payments'] == 'NaN':
		count_NaN_payments += 1


print "number of POIs:", count_poi
print "total value of the stock belonging to James Prentice:", enron_data["PRENTICE JAMES"]['total_stock_value']
print "number of email messages from Wesley Colwell to POIs:", enron_data['COLWELL WESLEY']['from_this_person_to_poi']
print "value of stock options exercised by Jeffrey Skilling:", enron_data['SKILLING JEFFREY K']['exercised_stock_options']
print "number of folks have a quantified salary", count_salary
print "number of folks have a known email_address", count_email
print "number of folks have NaN for total_payments", count_NaN_payments

