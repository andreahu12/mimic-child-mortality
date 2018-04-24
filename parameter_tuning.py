import pandas as pd
import numpy as np
import math
from time import time
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression


# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")
def load_data():
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

    feature = np.delete(bal_data, 2, 1).astype('int')
    label = bal_data[:, 2].astype('int')

    # train_rows = int(math.floor(0.8* bal_data.shape[0]))
    # # test_rows = bal_data.shape[0] - train_rows
    #
    # trainX = feature[:train_rows]
    # trainY = label[:train_rows]
    # trainY = trainY.astype('int')
    # testX = feature[train_rows:]
    # testY = label[train_rows:]
    # testY = testY.astype('int')
    #
    # ratio = testY[np.where( testY[:] == 1)].size/float(testY.size)
    # print 'dead patients accounts for: ', ratio
    return feature, label

if __name__ == '__main__':
    print "loading data"
    X, y = load_data()

    print "X.shape:", X.shape
    print "y.shape:", y.shape
    num_samples, num_features = X.shape

    print "--------------------------------------------"
    print "tuning random forest classifier"
    # build a classifier
    # use a full grid over all parameters
    depths = range(50, num_features + 1, 50)
    depths.extend([1, None])
    rf_param_grid = {"max_depth": depths,
                    "n_estimators": range(10, num_samples + 1, 10),
                    "criterion": ["gini", "entropy"]}
    print "rf_param_grid:", rf_param_grid
    clf = RandomForestClassifier()
    # print clf.get_params()
    # run grid search
    grid_search = GridSearchCV(clf, param_grid=rf_param_grid)
    start = time()
    grid_search.fit(X, y)
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)

    print "--------------------------------------------"
    print "tuning support vector classifier"
    possible_c = [round(0.1 * x, 1) for x in range(1, 11, 1)]

    svc_param_grid = {"kernel": ['linear', 'poly', 'rbf', 'sigmoid'],
                    "C": possible_c}
    print "svc_param_grid:", svc_param_grid
    clf = SVC()
    # print clf.get_params()
    # run grid search
    grid_search = GridSearchCV(clf, param_grid=svc_param_grid)
    start = time()
    grid_search.fit(X, y)
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)

    print "--------------------------------------------"
    print "tuning logistic regression"
    possible_c = [round(0.1 * x, 1) for x in range(1, 11, 1)]
    solver_l1 = ['liblinear', 'saga']
    solver_l2 = ['newton-cg', 'lbfgs', 'sag']
    lr_param_grid_l1 = {"penalty": ['l1'], "C": possible_c, "solver": solver_l1}
    lr_param_grid_l2 = {"penalty": ['l2'], "C": possible_c, "solver": solver_l2}

    print "lr_param_grid_l1:", lr_param_grid_l1

    clf = LogisticRegression()
    # print clf.get_params()
    grid_search = GridSearchCV(clf, param_grid=lr_param_grid_l1)
    start = time()
    grid_search.fit(X, y)
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)

    print "\nlr_param_grid_l2:", lr_param_grid_l2
    grid_search = GridSearchCV(clf, param_grid=lr_param_grid_l2)
    start = time()
    grid_search.fit(X, y)
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)
