from datetime import datetime
from os import path
import json
from time import sleep

def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')

def loadJson(loader, fileName, sorted={False:''}):
    fileName = fileName + ".json"
    if(path.exists(fileName)):
        print("loading from file")
        file = open(fileName,"r")
        results = json.load(file)
    else:
        print("reading through API")
        results = loader()
        file = open(fileName,"w")
        json.dump(results,file)
        if(sorted[0]):
            results.sort(key=lambda x: x.get(sorted[1]))
            json.dump(results,file)
            
    return results