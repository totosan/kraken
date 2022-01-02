import json
from os import path, listdir
from typing import Optional

from pandas.core.frame import DataFrame

from utils import DEFAULT_DATA_DIR
from BaseQuery import BaseQuery
from CsvExport import CsvExportEnum
    
class TradeHistory(BaseQuery):
    def __init__(self, config=None):
        if(not config):
            config = {'trades':True, 'ofs':0}

        super().__init__(config)
        self._apiName = "TradesHistory"
        self._resultSetName = "trades"
        
    def get_query_results(self):
        return super().get_from_API()
    
    def get_from_Export(self,startDate=None, endDate=None)-> Optional[DataFrame]:
        return super().Get_from_Export(CsvExportEnum.trades, startDate, endDate)
