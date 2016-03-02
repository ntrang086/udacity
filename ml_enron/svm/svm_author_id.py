#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

#########################################################

from sklearn.svm import SVC

"""
Using a linear kernel
clf = SVC(kernel="linear")

### the time to train and test the algorithm
t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

t1 = time()
pred = clf.predict(features_test)
print "predicting time:", round(time()-t1, 3), "s"


### find the accuracy score
from sklearn.metrics import accuracy_score
print accuracy_score(labels_test, pred)

"""

### Using an rbf kernel, C = 10000
clf = SVC(kernel="rbf", C=10000)


"""
and 1% of training data set

features_train = features_train[:len(features_train)/100]
labels_train = labels_train[:len(labels_train)/100] 
"""

t0 = time()

clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"
pred = clf.predict(features_test)


### find the accuracy score
from sklearn.metrics import accuracy_score
print accuracy_score(labels_test, pred)

### predict the elements, 1 means Chris, 0 means Sarah
print "predict 10th element:", clf.predict(features_test[10])
print "predict 26th element:", clf.predict(features_test[26])
print "predict 50th element:", clf.predict(features_test[50])
