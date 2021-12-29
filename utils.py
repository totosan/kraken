from datetime import datetime
from os import path
import json
from time import sleep

def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')

def loadJson(loader, fileName, sorted={False,''}):
    fileName = fileName + ".json"
    if(path.exists(fileName)):
        print("loading from file")
        file = open(fileName,"r")
        results = json.load(file)
    else:
        print("reading through API")
        results = loader()
        if(sorted[0]):
            results.sort(key=lambda x: x.get(sorted[1]))
        print(f'There {len(results)} trades in history')
        full, rest = divmod(len(results) , 50)
        pages = full + rest
        print(f'Fetched {pages} pages')
        #for v in trades:
        #    time = datetime.utcfromtimestamp(v["time"]).strftime('%Y-%m-%dT%H:%M:%SZ')
        #    print(f'{v}')
        file = open(fileName,"w")
        json.dump(results,file)
        print("Wait 10s for decharge rate limits..")
        sleep(10)