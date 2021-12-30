import krakenex
from BaseQuery import BaseQuery
import utils

DEBUG = True
class OrderState():
    open = "open"
    closed = "closed"
    pending = "pending"
    canceled = "canceled"
    expired = "expired"
        
class ClosedOrders(BaseQuery):
    def __init__(self,config=None):
        
        if(not config):
            config = {'trades':True, 'ofs':0}
        super().__init__(config=config)
        self._apiName = "ClosedOrders"
        self._resultSetName = "closed"
        
    def get_query_results(self):
        return super().get_from_API()

class OpendOrders(BaseQuery):
    def __init__(self,config=None):
        
        if(not config):
            config = {'trades':True, 'ofs':0}
        super().__init__(config=config)
        self._apiName = "OpenOrders"
        self._resultSetName = "open"
        
    def get_query_results(self):
        return super().get_from_API()
