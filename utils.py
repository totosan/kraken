from datetime import datetime
from os import path, mkdir
import json
from time import sleep,mktime


def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')
def dateTime2Posix(datetimeString):
    return mktime(datetime.fromisoformat(datetimeString).timetuple())

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
            try:
                if(sorted):
                    results.sort(key=lambda x: x.get(sorted))
            except Exception as e:
                print(e)
                
            json.dump(results, file)
            file.flush()

    return results
