from os import path

from BaseQuery import BaseQuery
from CsvExport import ExportEnum
    
class TradeHistory(BaseQuery):
    def __init__(self, config=None):
        if(not config):
            config = {'trades':True, 'ofs':0}

        super().__init__(config)
        self._apiName = "TradesHistory"
        self._resultSetName = "trades"
        
    def get_query_results(self):
        return super().get_from_API()
    
    def get_from_Export(self):
        filename = super()._get_export_from_API(ExportEnum.trades)
        return super()._get_from_zip(filename)
