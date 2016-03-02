#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot
from sklearn.decomposition import PCA
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


# Function used to create a new feature later
def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """

    fraction = 0.
    if (poi_messages != 'NaN' or all_messages != 'NaN') and all_messages != 0:
        fraction = float(poi_messages)/(all_messages)


    return fraction


### Task 0: Data exploration

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


print " *** DATA EXPLORATION ***\n"
print "number of people (data points):", len(data_dict)

count_poi = 0
count_salary = 0
count_email = 0
count_NaN_payments = 0
print "number of features per person:", len(data_dict['METTS MARK'])
for person in data_dict:
	if data_dict[person]['poi'] == True:
		count_poi += 1
	if data_dict[person]['salary'] != 'NaN':
		count_salary += 1
	if data_dict[person]['email_address'] != 'NaN':
		count_email += 1
	if data_dict[person]['total_payments'] == 'NaN':
		count_NaN_payments += 1

print "number of POIs:", count_poi
print "number of POIs:", len(data_dict) - count_poi
print "number of folks have a quantified salary", count_salary
print "number of folks have a known email_address", count_email
print "number of folks have NaN for total_payments", count_NaN_payments



### TASK 1: Remove outliers

### remove the TOTAL line
data_dict.pop('TOTAL', 0)


#TEST OUTLIERS BY PAIR
# tested "salary" against: "bonus", 'deferral_payments', 'total_payments', 'loan_advances', "total_stock_value"
# max deferral_payments: FREVERT MARK A
# max total payments, loan_advances, total_stock_value: LAY KENNETH L
# tested: ["to_messages", "from_messages"]
# max "from_poi_to_this_person": LAVORATO JOHN J
# max "from_this_person_to_poi"; DELAINEY DAVID W


features_outlier_test = ["from_this_person_to_poi", "from_poi_to_this_person"]

data = featureFormat(data_dict, features_outlier_test)

for point in data:
    salary = point[0]
    bonus = point[1]
    matplotlib.pyplot.scatter( salary, bonus )

matplotlib.pyplot.xlabel("from_this_person_to_poi")
matplotlib.pyplot.ylabel("from_poi_to_this_person")
matplotlib.pyplot.show()


person = max(data_dict, key=lambda person: data_dict[person]['from_poi_to_this_person']
	if isinstance(data_dict[person]["from_poi_to_this_person"], int)
	else float("-inf"))

print person, data_dict[person]




"""
Features in the data set

financial features: ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 
'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 
'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

email features: ['to_messages', 'email_address', 'from_poi_to_this_person', 'from_messages', 
'from_this_person_to_poi', 'poi', 'shared_receipt_with_poi']
"""


### TASK 2: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict
for name in data_dict:
	data_point = data_dict[name]
	from_poi_to_this_person = data_point["from_poi_to_this_person"]
	to_messages = data_point["to_messages"]
	fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
	data_point["fraction_from_poi"] = fraction_from_poi

	from_this_person_to_poi = data_point["from_this_person_to_poi"]
	from_messages = data_point["from_messages"]
	fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
	data_point["fraction_to_poi"] = fraction_to_poi
	my_dataset[name]["fraction_from_poi"] = fraction_from_poi
	my_dataset[name]["fraction_to_poi"] = fraction_to_poi



### Draw a scatter plot to show fraction_from_poi and fraction_to_poi
features_email_poi = ["poi", "fraction_from_poi", "fraction_to_poi"]

data = featureFormat(my_dataset, features_email_poi)

for point in data:
    salary = point[1]
    bonus = point[2]
    if point[0] == 1.0: # if poi, make it red
    	matplotlib.pyplot.scatter( salary, bonus, color="r" )
    else:
    	matplotlib.pyplot.scatter( salary, bonus )

matplotlib.pyplot.xlabel("fraction_from_poi")
matplotlib.pyplot.ylabel("fraction_to_poi")
matplotlib.pyplot.show()




### TASK 3: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".



""" COMPLETE LIST OF FEATURES
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 
'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 
'other', 'long_term_incentive', 'restricted_stock', 'director_fees', 'fraction_to_poi', 'fraction_from_poi', 'shared_receipt_with_poi']

"""

### Chosen features, based on Feature Selection step below
features_list = ['poi', 'salary', 'fraction_to_poi', 'total_stock_value', 'shared_receipt_with_poi']

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


### Feature scaling
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
features = scaler.fit_transform(features)


"""
### Perform PCA

pca = PCA(n_components=2)
pca.fit(features)
print pca.explained_variance_ratio_
first_pc = pca.components_[0]
second_pc = pca.components_[1]
print first_pc, second_pc

transformed_features = pca.transform(features)
plt = matplotlib.pyplot
#print features, transformed_features
#print zip(transformed_features, features)
for i, j in zip(transformed_features, features):
	plt.scatter(first_pc[0]*i[0], first_pc[1]*i[0], color="r")
	plt.scatter(second_pc[0]*i[0], second_pc[1]*i[0], color="c")
	plt.scatter(j[0], j[1], color="b") # the dots represent original values of bonus and long-term incentive
plt.xlabel("bonus")
plt.ylabel("long_term_incentive")
plt.show()

"""


### TASK 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html



from sklearn import tree
clf = tree.DecisionTreeClassifier(min_samples_split=22) 


# min_samples_split = 25: Accuracy: 0.83021	Precision: 0.40968	Recall: 0.42750	F1: 0.41840	F2: 0.42381
# 24: Accuracy: 0.83079	Precision: 0.41301	Recall: 0.43800	F1: 0.42514	F2: 0.43276
# 23: Accuracy: 0.83007	Precision: 0.41157	Recall: 0.44100	F1: 0.42578	F2: 0.43478
# 22: Accuracy: 0.83007	Precision: 0.41166	Recall: 0.44150	F1: 0.42606	F2: 0.43519  --- best option
# 21: Accuracy: 0.82950	Precision: 0.40954	Recall: 0.43800	F1: 0.42329	F2: 0.43200



### TASK 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)


""" #Tried KFold. Doesn't make any difference
#print len(labels)
#132 data points
from sklearn.cross_validation import KFold
kf = KFold(len(labels), n_folds=6, shuffle=True)
for train_index, test_index in kf:
	# make training and testing datasets
	print("TRAIN:", train_index, "TEST:", test_index)
	features_train = [features[i] for i in train_index]
	features_test = [features[i] for i in test_index]
	labels_train = [labels[i] for i in train_index]
	labels_test = [labels[i] for i in test_index]

"""

"""
from sklearn.grid_search import GridSearchCV
parameters = {'criterion':('gini', 'entropy'), 'splitter':('best', 'random'), 'max_depth': (None, 2, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
'min_samples_split': (2, 5, 10, 15, 20, 22, 25, 30)}

# 'min_weight_fraction_leaf' must be in [0, 0.5]
# max_leaf_nodes 1 must be either smaller than 0 or larger than 1
# either use max_leaf_nodes or max_depth

grid_search_clf = GridSearchCV(clf, parameters)
grid_search_clf.fit(features_train, labels_train)
print grid_search_clf.best_estimator_

"""


"""
Conclusions: splitter HAS TO be 'best', max_depth doesn't matter. Still not sure why the best_estimator_ keeps showing splitter as 'random'
Default tree:
DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
            max_features=None, max_leaf_nodes=None, min_samples_leaf=1,
            min_samples_split=22, min_weight_fraction_leaf=0.0,
            random_state=None, splitter='best')

Initially included all the parameters:
parameters = {'criterion':('gini', 'entropy'), 'splitter':('best', 'random'), 'max_depth': (None, 2, 5, 10, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30),
'min_weight_fraction_leaf': (0., 0.1, 0.2, 0.3, 0.4, 0.5), 'min_samples_split': (2, 5, 10, 15, 20, 22, 25, 30),
'min_samples_leaf': (1, 2, 5, 10, 15, 20, 25, 30), 'random_state': (None, 10, 20, 30, 40)}

"""

#TRIED GridSearchCV for SVC, but it's too slow


"""
### Feature selection,  using the complete list of features from line 158
### Do this here because data set needs splitting up into train and test first

### Use SelectKBest. SelectPercentile produces the same scores
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(f_classif, k=5)
selector.fit(features_train, labels_train)

features_train = selector.transform(features_train)
features_test = selector.transform(features_test)

### Identify chosen features
feature_mapping = dict(zip(features_list[1:], selector.get_support()))
print feature_mapping
print [k for k, v in feature_mapping.iteritems() if v == True]

### Get scores for features
features_scores = dict(zip(features_list[1:], selector.scores_))

features_pvalues_ = dict(zip(features_list[1:], selector.pvalues_))
#print features_pvalues_
top_features = sorted(features_scores.iteritems(), key=lambda x:-x[1])[:5]
print "Top features:"
for feature in top_features:
	print "{0}: {1}".format(*feature), ", p-value = ", round(features_pvalues_[feature[0]], 7)

"""

""" RESULTS FROM SelectKBest
{'salary': 15.806090087437418, 'fraction_from_poi': 0.49060990360486301, 'deferral_payments': 0.0098194464190455126, 
'total_payments': 8.9627155009973993, 'exercised_stock_options': 9.9561675820785211, 'bonus': 30.652282305660439, 
'director_fees': 1.6410979261701475, 'restricted_stock_deferred': 0.67928033895169282, 'total_stock_value': 10.814634863040405, 
'expenses': 4.3143955730810664, 'fraction_to_poi': 13.791413236761116, 'loan_advances': 7.0379327981934612, 'other': 3.1966845043285219, 
'deferred_income': 8.4934970305461821, 'shared_receipt_with_poi': 10.669737359602689, 'restricted_stock': 8.0511018969982544, 
'long_term_incentive': 7.5345222400328424}
Top 5 features: 
bonus: 30.6522823057 , p-value =  2.58451946415e-07
salary: 15.8060900874 , p-value =  0.000134321523395
fraction_to_poi: 13.7914132368 , p-value =  0.000339568747843
total_stock_value: 10.814634863 , p-value =  0.00139929018995
shared_receipt_with_poi: 10.6697373596 , p-value =  0.00150147878585

#feature selection: bonus has a very high score, and p-value << 0.05. however it reduces the accuracy???"

"""




### TASK 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
