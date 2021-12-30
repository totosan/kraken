from os import path
from BaseQuery import BaseQuery
from CsvExport import ExportEnum
    
class Ledgers(BaseQuery):
    def __init__(self, config=None):
        super().__init__(config)
        self._apiName = "Ledgers"
        self._resultSetName = "ledger"
        
    def get_query_results(self):
        return super().get_from_API()
    
    def get_from_Export(self,startDate=None, endDate=None):
        filename = super()._query_export(ExportEnum.ledgers,startDate=startDate,endDate=endDate)
        return super()._get_from_zip(filename)