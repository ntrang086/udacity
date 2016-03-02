#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 


from sklearn import cross_validation
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=42)

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score
print "accuracy score:", accuracy_score(labels_test, pred)
print "precision score:", precision_score(labels_test, pred)
print "recall score:", recall_score(labels_test, pred)


import numpy
print "number of POIs that are predicted for the test set for your POI identifier:", numpy.count_nonzero(pred)
print "number of POIs that are in the test set:", numpy.count_nonzero(labels_test)
print "total number of people in test set:", len(labels_test) 
print "If your identifier predicted 0 for everyone in the test set, its accuracy would be:", float(25.0/29.0)

### other practice
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
print "accuracy score:", accuracy_score(true_labels, predictions)
print "precision score:", precision_score(true_labels, predictions)
print "recall score:", recall_score(true_labels, predictions)