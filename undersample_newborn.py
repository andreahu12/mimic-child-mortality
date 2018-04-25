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

l_AUC = []
l_accu = []
l_f1 = []
l_rec = []
l_precision = []


for i in range(3):
    # data = pd.read_csv('/Users/quanquan/Documents/6250project/mimic-child-mortality/newborns.txt', header = None)
    data = pd.read_csv('newborns.txt', header = None)
    data = data.values
    for i in range(418):
        if type(data[0,i]) == str and i!= 2 and i!=3:
            for j in range(8100):
                data[j,i] = float(data[j,i].replace("[","").replace("(","").replace("]","").replace(")",""))
    for j in range(8100):
        data[j,2] = 0 if data[j,2] == "u'F'" else 1
        data[j,3] = 0 if data[j,3] == ' False' else 1

    data = data[:,1:] #delete the first column

    dead_patients = data[np.where( data[:,2] == 1)]
    print dead_patients.shape
    alive_patients = data[np.where( data[:,2] == 0)]
    print alive_patients.shape
    
    np.random.shuffle(alive_patients)
    alive_patients = alive_patients[:64] #randomly select same number of patients as that of dead data.

    bal_data = np.concatenate((dead_patients, alive_patients), axis=0) # dataset contains balanced data.
    np.random.shuffle(bal_data)

    feature = np.delete(bal_data, 2, 1)
    label = bal_data[:, 2]

    train_rows = int(math.floor(0.8* bal_data.shape[0]))
    print train_rows
    # test_rows = bal_data.shape[0] - train_rows

    trainX = feature[:train_rows]
    trainY = label[:train_rows]
    trainY = trainY.astype('int')
    testX = feature[train_rows:]
    testY = label[train_rows:]
    testY = testY.astype('int')
    print testY.shape
    print trainY.shape

    ratio = testY[np.where( testY[:] == 1)].size/float(testY.size)
    print 'dead patients accounts for: ', ratio



    # ########## SVM @#############
    # clf = svm.SVC(kernel='linear', C= 0.5).fit(trainX, trainY)
    # predY = clf.predict(testX)
    
    ########## Logistic Regression @#############
    clf = linear_model.LogisticRegression(penalty='l2',C=0.5, solver= "liblinear")
    clf.fit(trainX, trainY)
    predY = clf.predict(testX)
    
    # ########## Random Forest @#############
    # clf = RandomForestClassifier(n_estimators=30, criterion='entropy', max_depth=250)
    # clf.fit(trainX, trainY)
    # predY = clf.predict(testX)
    # 

    # AUC
    fpr, tpr, thresholds = metrics.roc_curve(testY, predY, pos_label=1)
    AUC = metrics.auc(fpr, tpr)
    print "AUC: ", AUC
    l_AUC.append(AUC)

    # Recall score
    rec_score = recall_score(testY, predY, average='macro')
    print "recall score: ", rec_score
    l_rec.append(rec_score)

    # precision
    p = precision_score(testY, predY) 
    print 'precision:', p 
    l_precision.append(p)
    
    # accuracy
    accu_score = accuracy_score(testY, predY)
    print "accuracy: ", accu_score
    l_accu.append(accu_score)


    # F1 score
    f1 = f1_score(testY, predY, average='macro')
    print "F1 score: ", f1
    l_f1.append(f1)


print  np.mean(l_accu),np.mean(l_precision), np.mean(l_rec), np.mean(l_f1), np.mean(l_AUC)
print  np.std(l_accu), np.std(l_precision), np.std(l_rec), np.std(l_f1), np.std(l_AUC)


