import krakenex

class OrderState():
    open = "open"
    closed = "closed"
    pending = "pending"
    canceled = "canceled"
    expired = "expired"
        
class Orders(object):
    
    def __init__(self, *args):
        k = krakenex.API()
        k.load_key('kraken.key')
        self.__countOpenOrders = 0
        self.__countClosedOrders =0
        
        options = {'trades':True}
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
        orders = self.__orders
        for _, o in orders.items():
            if(o["status"] == orderstate):
                print(o['descr']['order'])
    
