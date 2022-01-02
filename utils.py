from datetime import datetime
from os import path, mkdir
import json
from time import sleep,mktime
import calendar

DEFAULT_DATA_DIR = './data/'

def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')
def dateTime2Posix(datetimeString):
    return mktime(datetime.fromisoformat(datetimeString).timetuple())

# takes date and returns nix time
def date2nix(dateValue):
    return calendar.timegm(dateValue.timetuple())

# takes nix time and returns date
def nix2date(nix_time):
    return datetime.fromtimestamp(nix_time).strftime('%m, %d, %Y')


def lastState(loader, fileName, *loaderArgs, sorted=""):    
    defaultPath = DEFAULT_DATA_DIR
    if(not path.exists(defaultPath)):
        mkdir(defaultPath)
        
    fileName = path.join(defaultPath, fileName + '.json')
    if(path.exists(fileName)):
        print("loading from file")
        file = open(fileName, "r")
        results = json.load(file)
    else:
        print("reading through API")
        if(len(loaderArgs)>0):
           results = loader(*loaderArgs) 
        else:
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
