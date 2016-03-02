#!/usr/bin/python

import os
import pickle
import re
import sys

sys.path.append( "../tools/" )
from parse_out_email_text import parseOutText



"""
    Starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification.

    The list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    The actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project. If you have
    not obtained the Enron email corpus, run startup.py in the tools folder.

    The data is stored in lists and packed away in pickle files at the end.
"""


from_sara  = open("from_sara.txt", "r")
from_chris = open("from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list so you
### can iterate your modifications quicker


for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        path = os.path.join('..', path[:-1])
        email = open(path, "r")

        ### use parseOutText to extract the text from the opened email
        email_contents = parseOutText(email)

        ### use str.replace() to remove any instances of the words
        ### ["sara", "shackleton", "chris", "germani"]
        ### removing outliers (signature words)"sshacklensf", "cgermannsf" 
        ### see detail at https://www.udacity.com/course/viewer#!/c-ud120/l-2948958577/e-3014988626/m-3006998559
        ### the results will be different from answers in lesson 10 after removing outliers
        for word in ["sara", "shackleton", "chris", "germani", "sshacklensf", "cgermannsf"]:
            email_contents = email_contents.replace(word, "")
        
        ### remove double space
        email_contents = email_contents.replace("  ", " ")
        
        ### append the text to word_data
        word_data.append(email_contents)

        ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
        
        if name == "sara":
            from_data.append(0)
        else:
            from_data.append(1)
            
        email.close()

print "emails processed"

from_sara.close()
from_chris.close()

pickle.dump( word_data, open("your_word_data.pkl", "w") )
pickle.dump( from_data, open("your_email_authors.pkl", "w") )

print "word_data[152]:", word_data[152]



### in Part 4, do TfIdf vectorization here. also remove stop words
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words="english")
vectorizer.fit_transform(word_data)
feature_mapping = vectorizer.get_feature_names()
print "mapped features size:", len(feature_mapping)
print "feature_mapping[34597]:", feature_mapping[34597]

### note: ideally use regrex to remove the words. otherwise, replace will remove any instance of, say, sara
### whether it's a standalone word or part of another word. e.g. saraemail --> email
