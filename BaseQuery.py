from os import path
from time import sleep
import zipfile
import krakenex
from abc import ABC
class BaseQuery(ABC):
    
    def __init__(self, config=None):
        self._k = krakenex.API()
        self._k.load_key('kraken.key')
        
        self._apiName=""
        self._resultSetName=""
        
        self._queryOptions = {'ofs':0}
        if(not config is None):
            self._queryOptions.update( config)
        
    def _query(self,apiName, resultSetName,options):
        result = self._k.query_private(apiName,options)
        errorsPretty = ""
        if(len(result["error"])==0):
            result = result["result"][resultSetName]
        else:
            errorsPretty = "\n".join(result["error"])
            print(f'There were errors on reading Ledger API:{errorsPretty}')
        return errorsPretty, result
    
    def get_query_results(self):
        _, self._queryResult = self._query(self._apiName, self._resultSetName, self._queryOptions)
        count = len(self._queryResult)
        currentEntries = count
        allResults = []
        while (currentEntries>0):

            for k,v in self._queryResult.items():
                v['entity_id']=k
                allResults.append(v)

            self._queryOptions["ofs"]=count
            error, results = self._query(self._apiName, self._resultSetName,self._queryOptions)
            if(error):
                break;
            currentEntries = len(results) 
            count = count + currentEntries
            if(count % 100 == 0):
                print("possible limit exceed for querying API. waiting some seconds.")
                sleep(10)
            
        return allResults

    def get_from_Zip(self, filename):
        with zipfile.ZipFile(filename, "r") as zip:
            info=zip.infolist()
            for file in info:
                zip.extract(file.filename,path.dirname(filename))
