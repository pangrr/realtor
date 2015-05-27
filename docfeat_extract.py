#docfeat_extract.py

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import re
import sys



def file2labeledSentences (fileName):
    labeledSents = []
    labels = []
    for line in open (fileName, "r").readlines():
        arr = line.split (" ", 1)
        label = arr[0]
        labels.append(label)
        wordArr = re.sub ("[^0-9a-zA-Z]+", " ", arr[1]).split()
        labeledSents.append (LabeledSentence(words=wordArr, labels=[label]))
    return (labeledSents, labels)





def getFeat (labeledSents, labels, outputFileName):
    model = Doc2Vec (labeledSents, size=20)
    file = open(outputFileName, "w")
    for label in labels:
        try:
            file.write (label + " " + " ".join(map(str, model[label])) + "\n")
        except KeyError:
            print (label)




if __name__ == "__main__":
    labeledSents, labels = file2labeledSentences (sys.argv[1])
    getFeat (labeledSents, labels, sys.argv[1] + "_feat")
