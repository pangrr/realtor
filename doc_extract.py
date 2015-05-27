# doc_extract.py

import os
import sys
import json

output = {}
for fileName in os.listdir(sys.argv[1]):
    if fileName == ".DS_Store" or fileName == sys.argv[1]:
        continue
    input = json.loads(open(sys.argv[1]+"/"+fileName, "r").read())
    if "Description" in input:
        output[fileName] = input["Description"].replace("\n", " ").replace("\r", " ")

writeFile = open(sys.argv[1]+"_doc", "w")
for key in output:
    writeFile.write(key+" "+output[key] + "\n")
