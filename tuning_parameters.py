# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from sklearn import svm
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier

# data = pd.read_csv('/Users/quanquan/Documents/Project/mimic-child-mortality/features.txt', header = None)
data = pd.read_csv('features.txt', header = None)

data = data.values
for i in range(418):
    if type(data[0,i]) == str and i!= 2 and i!=3:
        for j in range(8200):
            data[j,i] = float(data[j,i].replace("[","").replace("(","").replace("]","").replace(")",""))
for j in range(8200):
    data[j,2] = 0 if data[j,2] == "u'F'" else 1
    data[j,3] = 0 if data[j,3] == ' False' else 1


data = data[:,1:] #delete the first column

dead_patients = data[np.where( data[:,2] == 1)]

alive_patients = data[np.where( data[:,2] == 0)]
np.random.shuffle(alive_patients)
alive_patients = alive_patients[:73] #randomly select same number of patients as that of dead data.

bal_data = np.concatenate((dead_patients, alive_patients), axis=0) # dataset contains balanced data.
np.random.shuffle(bal_data)

feature = np.delete(bal_data, 2, 1)
label = bal_data[:, 2]

label = label.astype('int')

## SVM
for Kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
    clf = svm.SVC(kernel=Kernel, C= 0.5)
    scores = cross_val_score(clf, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

for c in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    clf = svm.SVC(kernel='linear', C= 0.5)
    scores = cross_val_score(clf, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
    
## LR
for p in ['l1','l2']:
    logreg = linear_model.LogisticRegression(penalty=p)    
    scores = cross_val_score(logreg, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

for c in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    logreg = linear_model.LogisticRegression(penalty='l2',C=c)    
    scores = cross_val_score(logreg, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

for s in ['liblinear', 'saga', 'newton-cg', 'lbfgs', 'sag']:
    logreg = linear_model.LogisticRegression(penalty='l2',C=0.5, solver= s)    
    scores = cross_val_score(logreg, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


    

# Random Forest
for n in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]:
    clf = RandomForestClassifier(n_estimators=n)
    scores = cross_val_score(clf, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

for c in ['gini', 'entropy']:
    clf = RandomForestClassifier(n_estimators= 30, criterion=c)
    scores = cross_val_score(clf, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
for depth in [1, 50, 100, 150, 200, 250, 300, 350, 400, None]:
    clf = RandomForestClassifier(n_estimators=30, criterion='entropy', max_depth= depth)
    scores = cross_val_score(clf, feature, label, cv=3)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
