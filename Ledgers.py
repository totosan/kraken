from os import path
from BaseQuery import BaseQuery
    
class Ledgers(BaseQuery):
    def __init__(self, config=None):
        super().__init__(config)
        self._apiName = "Ledgers"
        self._resultSetName = "ledger"
        
    def get_query_results(self):
        return super().get_from_API()
    