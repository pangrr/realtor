# lasso_split.py

from sklearn import linear_model
import numpy as np
import sys
import os




def loadData (featFile, trainFile, testFile):
    feats = file2dict (featFile)
    train = file2dict (trainFile)
    test = file2dict (testFile)
    trainX = buildX (feats, train)
    trainY = buildY (train)
    testX = buildX (feats, test)
    testY = buildY (test)
    return (trainX, trainY, testX, testY)





def file2dict (file):
    dict = {}
    for line in open (file, "r").read().splitlines():
        arr = line.strip().split()
        key = arr.pop (0)
        dict[key] = arr
    return dict




def buildX (feats, train):
    nFeat = len (next(iter(feats.values())))
    nLine = len (train)
    X = np.zeros ([nLine, nFeat])
    i = 0
    for ID in train:
        try:
            feat = feats[ID]
            for j in range (nFeat):
                X[i][j] = float (feat[j])
            i += 1
        except KeyError:
            print (ID)
    return X


def buildY (train):
    y = np.zeros (len(train))
    i = 0
    for ID in train:
        y[i] = float (train[ID][0].replace(",", ""))
        i += 1
    return y



def frange(start, stop, step):
     i = start
     while i < stop:
         yield i
         i += step


def train (X, y, a):
    clf = linear_model.Lasso(alpha=a, max_iter=5000)
    clf.fit(X, y)
    return clf


def mse (t, y):
    sum = 0.0
    for i in range(len(t)):
        sum += (t[i]-y[i]) * (t[i]-y[i])
    return sum / len(t)





if __name__ == "__main__":
    featFile = sys.argv[1]
    trainDir = sys.argv[2] + "/"
    testDir = sys.argv[3] + "/"
    mseFile = open(sys.argv[4], "w")


    for fileName in os.listdir(trainDir):
        if fileName == ".DS_Store":
            continue

        trainX, trainY, testX, testY = loadData (featFile, trainDir + fileName, testDir + fileName)

        # search for best alpha
        bestA = 0.0
        minCost = 1000000000

        for a in frange(0.01, 10.0, 0.01):
            clf = train (trainX, trainY, a)

            #print (clf.coef_)
            #print (clf.intercept_)

            pred = clf.predict (testX)
            #print (pred)
            cost = mse (pred, testY)

            if cost < minCost:
                minCost = cost
                bestA = a

        mseFile.write (fileName + " " + str(minCost) + "\n")
