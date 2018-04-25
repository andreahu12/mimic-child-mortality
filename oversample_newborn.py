import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score


from sklearn.metrics import average_precision_score

l_AUPRC = []
l_rec = []
l_precision = []


# data = pd.read_csv('/Users/quanquan/Documents/6250project/mimic-child-mortality/newborns.txt', header = None)
data = pd.read_csv('newborns.txt', header = None)

# new borns
data = data.values
for i in range(418):
    if type(data[0,i]) == str and i!= 2 and i!=3:
        for j in range(8100):
            data[j,i] = float(data[j,i].replace("[","").replace("(","").replace("]","").replace(")",""))
for j in range(8100):
    data[j,2] = 0 if data[j,2] == "u'F'" else 1
    data[j,3] = 0 if data[j,3] == ' False' else 1

dead_patients = data[np.where( data[:,3] == 1)]
alive_patients = data[np.where( data[:,3] == 0)] 
os_dead_patients = dead_patients   
  
# oversample:
for i in xrange(7900):
    if i%100 ==0:
        print i
    n = np.random.randint(64)
    temp = dead_patients[n:n+1, :]
    os_dead_patients = np.concatenate((os_dead_patients, temp), axis=0)

dead_patients = os_dead_patients
print dead_patients.shape

dead_patients = dead_patients[:,1:] #delete the first column
alive_patients = alive_patients[:,1:] #delete the first column

for i in range(3):
    np.random.shuffle(dead_patients)   
    np.random.shuffle(alive_patients)   

    dead_feature = np.delete(dead_patients, 2, 1)
    dead_label = dead_patients[:, 2]
    dead_train_rows = int(math.floor(0.8* dead_patients.shape[0]))
    
    dead_trainX = dead_feature[:dead_train_rows]
    dead_trainY = dead_label[:dead_train_rows]
    dead_trainY = dead_trainY.astype('int')
    dead_testX = dead_feature[dead_train_rows:]
    dead_testY = dead_label[dead_train_rows:]
    dead_testY = dead_testY.astype('int')

    alive_feature = np.delete(alive_patients, 2, 1)
    alive_label = alive_patients[:, 2]
    alive_train_rows = int(math.floor(0.8* alive_patients.shape[0]))
    
    alive_trainX = alive_feature[:alive_train_rows]
    alive_trainY = alive_label[:alive_train_rows]
    alive_trainY = alive_trainY.astype('int')
    alive_testX = alive_feature[alive_train_rows:]
    alive_testY = alive_label[alive_train_rows:]
    alive_testY = alive_testY.astype('int')

    trainX = np.concatenate((dead_trainX, alive_trainX), axis=0) # dataset contains balanced data.
    trainY = np.concatenate((dead_trainY, alive_trainY), axis=0)
    testX = np.concatenate((dead_testX, alive_testX), axis=0)
    testY = np.concatenate((dead_testY, alive_testY), axis=0)

    test_ratio = testY[np.where( testY[:] == 1)].size/float(testY.size)
    train_ratio = trainY[np.where( trainY[:] == 1)].size/float(trainY.size)
    print 'in test, dead patients:', test_ratio
    print 'in training, dead patients:', train_ratio

    ########## SVM @#############
    clf = svm.SVC(kernel='linear', C= 0.5).fit(trainX, trainY)
    predY = clf.predict(testX)
    
    # AUPRC
    # y_score = clf.predict_proba(testX) 
    y_score = clf.decision_function(testX)
    average_precision = average_precision_score(testY, y_score)
    print "AUPRC: ", average_precision
    l_AUPRC.append(average_precision)

    # Recall score
    rec_score = recall_score(testY, predY, average='macro')
    print "recall score: ", rec_score
    l_rec.append(rec_score)

    # precision
    p = precision_score(testY, predY) 
    print 'precision:', p 
    l_precision.append(p)

print np.mean(l_AUPRC), np.mean(l_rec), np.mean(l_precision), 
print np.std(l_AUPRC), np.std(l_rec), np.std(l_precision)

for i in range(3):
    np.random.shuffle(dead_patients)   
    np.random.shuffle(alive_patients)   

    dead_feature = np.delete(dead_patients, 2, 1)
    dead_label = dead_patients[:, 2]
    dead_train_rows = int(math.floor(0.8* dead_patients.shape[0]))
    
    dead_trainX = dead_feature[:dead_train_rows]
    dead_trainY = dead_label[:dead_train_rows]
    dead_trainY = dead_trainY.astype('int')
    dead_testX = dead_feature[dead_train_rows:]
    dead_testY = dead_label[dead_train_rows:]
    dead_testY = dead_testY.astype('int')

    alive_feature = np.delete(alive_patients, 2, 1)
    alive_label = alive_patients[:, 2]
    alive_train_rows = int(math.floor(0.8* alive_patients.shape[0]))
    
    alive_trainX = alive_feature[:alive_train_rows]
    alive_trainY = alive_label[:alive_train_rows]
    alive_trainY = alive_trainY.astype('int')
    alive_testX = alive_feature[alive_train_rows:]
    alive_testY = alive_label[alive_train_rows:]
    alive_testY = alive_testY.astype('int')

    trainX = np.concatenate((dead_trainX, alive_trainX), axis=0) # dataset contains balanced data.
    trainY = np.concatenate((dead_trainY, alive_trainY), axis=0)
    testX = np.concatenate((dead_testX, alive_testX), axis=0)
    testY = np.concatenate((dead_testY, alive_testY), axis=0)

    test_ratio = testY[np.where( testY[:] == 1)].size/float(testY.size)
    train_ratio = trainY[np.where( trainY[:] == 1)].size/float(trainY.size)
    print 'in test, dead patients:', test_ratio
    print 'in training, dead patients:', train_ratio

    ########## Logistic Regression @#############
    clf = linear_model.LogisticRegression(penalty='l2',C=0.5, solver= "liblinear")
    clf.fit(trainX, trainY)
    predY = clf.predict(testX)
    
    # AUPRC
    # y_score = clf.predict_proba(testX) 
    y_score = clf.decision_function(testX)
    average_precision = average_precision_score(testY, y_score)
    print "AUPRC: ", average_precision
    l_AUPRC.append(average_precision)

    # Recall score
    rec_score = recall_score(testY, predY, average='macro')
    print "recall score: ", rec_score
    l_rec.append(rec_score)

    # precision
    p = precision_score(testY, predY) 
    print 'precision:', p 
    l_precision.append(p)

print np.mean(l_AUPRC), np.mean(l_rec), np.mean(l_precision), 
print np.std(l_AUPRC), np.std(l_rec), np.std(l_precision)
    

for i in range(3):
    np.random.shuffle(dead_patients)   
    np.random.shuffle(alive_patients)   

    dead_feature = np.delete(dead_patients, 2, 1)
    dead_label = dead_patients[:, 2]
    dead_train_rows = int(math.floor(0.8* dead_patients.shape[0]))
    
    dead_trainX = dead_feature[:dead_train_rows]
    dead_trainY = dead_label[:dead_train_rows]
    dead_trainY = dead_trainY.astype('int')
    dead_testX = dead_feature[dead_train_rows:]
    dead_testY = dead_label[dead_train_rows:]
    dead_testY = dead_testY.astype('int')

    alive_feature = np.delete(alive_patients, 2, 1)
    alive_label = alive_patients[:, 2]
    alive_train_rows = int(math.floor(0.8* alive_patients.shape[0]))
    
    alive_trainX = alive_feature[:alive_train_rows]
    alive_trainY = alive_label[:alive_train_rows]
    alive_trainY = alive_trainY.astype('int')
    alive_testX = alive_feature[alive_train_rows:]
    alive_testY = alive_label[alive_train_rows:]
    alive_testY = alive_testY.astype('int')

    trainX = np.concatenate((dead_trainX, alive_trainX), axis=0) # dataset contains balanced data.
    trainY = np.concatenate((dead_trainY, alive_trainY), axis=0)
    testX = np.concatenate((dead_testX, alive_testX), axis=0)
    testY = np.concatenate((dead_testY, alive_testY), axis=0)

    test_ratio = testY[np.where( testY[:] == 1)].size/float(testY.size)
    train_ratio = trainY[np.where( trainY[:] == 1)].size/float(trainY.size)
    print 'in test, dead patients:', test_ratio
    print 'in training, dead patients:', train_ratio

    ########## Random Forest @#############
    clf = RandomForestClassifier(n_estimators=30, criterion='entropy', max_depth=250)
    clf.fit(trainX, trainY)
    predY = clf.predict(testX)
    
    # AUPRC
    y_score = clf.predict_proba(testX) 
    # y_score = clf.decision_function(testX)
    average_precision = average_precision_score(testY, y_score[:, 1])
    print "AUPRC: ", average_precision
    l_AUPRC.append(average_precision)

    # Recall score
    rec_score = recall_score(testY, predY, average='macro')
    print "recall score: ", rec_score
    l_rec.append(rec_score)

    # precision
    p = precision_score(testY, predY) 
    print 'precision:', p 
    l_precision.append(p)

print np.mean(l_AUPRC), np.mean(l_rec), np.mean(l_precision), 
print np.std(l_AUPRC), np.std(l_rec), np.std(l_precision)

