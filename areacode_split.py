# areacode_split.py

import sys


def loadData (file):
    data = {}
    for line in open (file, "r").read().splitlines():
        arr = line.strip().split()
        key = arr.pop (0)
        data[key] = arr
    return data



def split (data):
    splits = {}
    for ID in data:
        splitKey = data[ID][2]
        if splitKey in splits:
            splits[splitKey].append((ID, data[ID]))
        else:
            splits[splitKey] = []
    return splits



def write (splits, dir):
    for splitKey in splits:
        file = open(dir+splitKey, "w")
        print (splitKey, len(splits[splitKey]))
        for entry in splits[splitKey]:
            file.write (entry[0] + " " + " ".join(entry[1]) + "\n")


if __name__ == "__main__":
    data = loadData (sys.argv[1])
    write (split(data), sys.argv[2])

