from io import StringIO
from os import path
from time import sleep
import zipfile
import krakenex

from utils import *
from CsvExport import CsvExport, CsvExportEnum
import pandas as pd
from typing import Optional

class BaseQuery():
    
    def __init__(self, config=None):
        self._k = krakenex.API()
        self._k.load_key('kraken.key')
        
        self._apiName=""
        self._resultSetName=""
        
        self._queryOptions = {'ofs':0}
        if(not config is None):
            self._queryOptions.update( config)
        print(self._queryOptions)
        
    def _query(self,apiName, resultSetName,options):
        result = self._k.query_private(apiName,options)
        errorsPretty = ""
        if(len(result["error"])==0):
            result = result["result"][resultSetName]
        else:
            errorsPretty = "\n".join(result["error"])
            print(f'There were errors on reading Ledger API:{errorsPretty}')
        return errorsPretty, result
    
    def _query_export(self, exportType, startDate=None,endDate=None):
        dataHistory = CsvExport(exportType)
        id = lastState(dataHistory.RequestNewReport,"reportId_"+exportType, startDate, endDate)
        print('Wait for data to be ready',end='')
        while True:
            reportDetails = dataHistory.RetrieveReportBy(id)
            if(reportDetails['status'] == 'Queued'):
                print(".",end='')
                sleep(1)
            else:
                break
        zipName = dataHistory.SaveExportById(id)
        return zipName
    
    def get_from_API(self):
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

    def _get_from_zip(self, filename) -> Optional[pd.DataFrame]:
        input_zip=zipfile.ZipFile(filename,"r")
        datas = [input_zip.read(name).decode("utf-8") for name in input_zip.namelist()]
        if(len(datas)==1):
            dataIO = StringIO(datas[0])
            dataFrame = pd.read_csv(dataIO)
            return dataFrame
        else:
            return None
        
    def Get_from_Export(self, typeOfExport,startDate=None, endDate=None):
        reportIdFilename = path.join(DEFAULT_DATA_DIR,"reportId_"+typeOfExport+".json")
        if(path.exists(reportIdFilename)):
            print("Open Zip-File fore reading "+typeOfExport)
            with open(reportIdFilename) as reportIdFP:
                report_id = json.load(reportIdFP)
            
            zipFileName =path.join(DEFAULT_DATA_DIR,typeOfExport+"_"+report_id+".csv.zip")
        else:                
            zipFileName = self._query_export(typeOfExport,startDate=startDate,endDate=endDate)
        return self._get_from_zip(zipFileName)