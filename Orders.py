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
        self._apiName = "ClosedOrders"
        self._resultSetName = "closed"
        
        super().__init__(config=config)
        k = krakenex.API()
        k.load_key('kraken.key')
        self.__countOpenOrders = 0
        self.__countClosedOrders =0
        
        options = {'trades':True, 'ofs':0}
        self._queryConfig = options
        open_orders = k.query_private('OpenOrders',options)
        closed_orders = k.query_private('ClosedOrders', options)
        self.__orders ={}
        
        if(len(open_orders["error"])==0):
            if(len(closed_orders["error"])==0):
                open_orders = open_orders["result"]
                closed_orders = closed_orders["result"]
                self.__countOpenOrders = len(open_orders["open"])
                self.__countClosedOrders = len(closed_orders["closed"])
                
                for k,v in open_orders["open"].items():
                    self.__orders[k]=v
                for k,v in closed_orders["closed"].items():
                    self.__orders[k]=v
        
    def get_all_orders_by(self, orderstate ):
        count = len(self.__orders)
        currentEntries = count
        orders = self.__orders
        allOrders = []
        while (currentEntries>0):

            for k,v in self.__orders.items():
                v['order_id']=k
                allOrders.append(v)

            self._queryConfig["ofs"]=count
            error, self._ledger = self.(self._ledgerQueryOptions)
            if(error):
                break;
            currentEntries = len(self._ledger) 
            count = count + currentEntries
            
            if DEBUG:
                for _, o in orders.items():
                    if(o["status"] == orderstate):
                        print(_,o['descr']['order'], utils.posix2DateTime( o["closetm"]))
        return orders
    
