from os import path
from BaseQuery import BaseQuery
    
class TradeHistory(BaseQuery):
    def __init__(self, config=None):
        if(not config):
            config = {'trades':True, 'ofs':0}

        super().__init__(config)
        self._apiName = "TradesHistory"
        self._resultSetName = "trades"
        
    def get_query_results(self):
        return super().get_from_API()
    