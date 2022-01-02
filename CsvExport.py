#!/usr/bin/env python3
#
# Responses can be binary ZIP streams instead of the expected JSON,
# based on query parameters. A prime example is 'RetrieveReport':
#
# https://www.kraken.com/features/api#get-history-export
#
# This script shows how to "unpack" such a response. 
#
# Run unbuffered to see output as in happens:
# python -u export-csv-export.py

###################################
##       Library imports         ##
###################################

from json import JSONDecodeError
from os import path
from pprint import pprint
from time import sleep
from abc import ABC

from pipe import *
import krakenex

class CsvExportEnum(ABC):
    ledgers = "ledgers"
    trades = "trades"

class CsvExport():
    def __init__(self, kindOf, defaultSavePath="./data/"):
        self._kraken = krakenex.API()
        # NOTE: key must have the "Export data" permission.
        self._kraken.load_key('kraken.key')

        self._type = kindOf
        self._defaultSavePath = defaultSavePath
        
    def RequestNewReport(self, startTime=None, endTime=None):
        config = {
                'description': 'reporting',
                'report': self._type,
                'format': 'CSV',
            }
        if(startTime):
            config.update({'starttm':startTime})
        if(endTime):
            config.update({'endtm':endTime})
                          
        response = self._kraken.query_private(
            'AddExport',
            config,
        )
        report_id = response['result']['id']
        self.ReportId = report_id
        return report_id
    

    def RetrieveAllReports(self):
        response = []
        while True:
            response = self._kraken.query_private('ExportStatus', {'report': self._type})
            if len(response['error']) > 0 and response['error'][0] == 'EExport:Not ready':
                print('.', end='')
                sleep(10)
            else:
                print('')
                break
        return response
    
    def RetrieveReportBy(self, report_id):
        response = self.RetrieveAllReports()
        reportDetails = list(response['result'] | where(lambda x: x['id'] == str(report_id)) )
        if (len(reportDetails)==1):
            return reportDetails[0]
        else:
            raise ValueError(f'Awaited single result but got {len(reportDetails)}')

    def SaveExportById(self, report_id):
        # Expecting streamed binary response when query successful.
        try:
            response = self._kraken.query_private('RetrieveExport', {'id': report_id})
        except JSONDecodeError:
            export_bytes = self._kraken.response.content
            filename = self._type + '_' + str(report_id)+'.csv.zip'
            filename = path.join(self._defaultSavePath, filename)
            with open(filename, 'wb') as fd:
                fd.write(export_bytes)
            print('Done! Written as: '+filename)
            return filename
        else:
            pprint(response)
        return ''