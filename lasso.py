# lasso.py

from sklearn import linear_model
import numpy as np




def loadData (featFile, valFile, trainIDFile, testIDFile):
    feats = file2dict (featFile)
    vals = file2dict (valFile)
    trainID = file2list (trainIDFile)
    testID = file2list (testIDFile)
    trainX = buildX (feats, trainID)
    trainY = buildY (vals, trainID)
    testX = buildX (feats, testID)
    testY = buildY (vals, testID)
    return (trainX, trainY, testX, testY, testID)


def file2dict (file):
    dict = {}
    for line in open (file, "r").read().splitlines():
        arr = line.strip().split()
        key = arr.pop (0)
        dict[key] = arr
    return dict


def file2list (file):
    return open (file, "r").read().splitlines()


def buildX (feats, IDList):
    nFeat = len (next(iter(feats.values())))
    nLine = len (IDList)
    X = np.zeros ([nLine, nFeat])
    i = 0
    for ID in IDList:
        feat = feats[ID]
        for j in range (nFeat):
            X[i][j] = float (feat[j])
        i += 1
    return X


def buildY (vals, IDList):
    y = np.zeros (len(IDList))
    i = 0
    for ID in IDList:
        y[i] = float (vals[ID][0].replace(",", ""))
        i += 1
    return y



def frange(start, stop, step):
     i = start
     while i < stop:
         yield i
         i += step


def train (X, y, a):
    clf = linear_model.Lasso(alpha=a)
    clf.fit(X, y)
    return clf


def mse (t, y):
    sum = 0.0
    for i in range(len(t)):
        sum += (t-y) * (t-y)
    return sum / len(t)





if __name__ == "__main__":

    trainX, trainY, testX, testY, testID = loadData ("san-jose-420-fea.txt", "san-jose-420-price.txt", "san-jose-420-id_train.txt", "san-jose-420-id_val.txt")

    # test best alpha
    """
    for a in frange(0.1, 1.0, 0.1):
        clf = train (trainX, trainY, a)

        #print (clf.coef_)
        #print (clf.intercept_)

        score = clf.score (testX, testY)
        print (score)
    """

    # output prediction
    clf = train (trainX, trainY, 0.3)
    pred = clf.predict(testX)
    outFile = open ("prediction", "w")
    for i in range(len(pred)):
        outFile.write (testID[i] + " " + str(testY[i]) + " " + str(pred[i]) + "\n")
