#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
features = ["salary", "bonus"]

# remove the TOTAL outlier
data_dict.pop('TOTAL', 0)

data = featureFormat(data_dict, features)


### your code below
for point in data:
    salary = point[0]
    bonus = point[1]
    matplotlib.pyplot.scatter( salary, bonus )

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()

# find the max salary and max bonus
# nested dictionary; http://stackoverflow.com/questions/31795092/key-in-nested-dictionary-if-it-contains-nan-value
print max(data_dict, key=lambda person: data_dict[person]['salary']
	if isinstance(data_dict[person]['salary'], int)
	else float("-inf"))

print data_dict['SKILLING JEFFREY K']['salary']


print min(data_dict, key=lambda person: data_dict[person]['bonus']
	if isinstance(data_dict[person]['bonus'], int)
	else float("-inf"))

print data_dict['LAVORATO JOHN J']['bonus']