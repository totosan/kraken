from datetime import datetime
from os import path, mkdir
import json
from time import sleep


def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')


def lastState(loader, fileName, sorted="",defaultPath = './data/'):    
    if(not path.exists(defaultPath)):
        mkdir(defaultPath)
        
    fileName = path.join(defaultPath, fileName + '.json')
    if(path.exists(fileName)):
        print("loading from file")
        file = open(fileName, "r")
        results = json.load(file)
    else:
        print("reading through API")
        results = loader()
        with open(fileName, "w") as file:
            json.dump(results, file)
            sleep(3)
            if(sorted):
                results.sort(key=lambda x: x.get(sorted))
                json.dump(results, file)
            file.flush()

    return results
