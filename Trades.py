import krakenex

class TradeHistroy(object):
    
    def __init__(self, tradeConfig=None):
        self._k = krakenex.API()
        self._k.load_key('kraken.key')

        self._tradesQueryOptions = {'ofs':0}
        if(not tradeConfig is None):
            self._tradesQueryOptions.update( tradeConfig)
            
        _, self._trades = self.queryTradeHistory(self._tradesQueryOptions)

    def queryTradeHistory(self, options):
        trades = self._k.query_private('TradesHistory',options)
        errorsPretty = ""
        if(len(trades["error"])==0):
            trades = trades["result"]["trades"]
        else:
            errorsPretty = "\n".join(trades["error"])
            print(f'There were errors on reading TradesHistory API:{errorsPretty}')
        return errorsPretty, trades
    
    def get_tradesHistory(self):
        count = len(self._trades)
        currentEntries = count
        allTrades = []
        while (currentEntries>0):

            for k,v in self._trades.items():
                v['trades_id']=k
                allTrades.append(v)

            self._tradesQueryOptions["ofs"]=count
            error, self._trades = self.queryTradeHistory(self._tradesQueryOptions)
            if(error):
                break;
            currentEntries = len(self._trades) 
            count = count + currentEntries
            
        return allTrades
            