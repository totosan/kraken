import krakenex

class Ledger(object):
    
    def __init__(self, ledgerConfig=None):
        self._k = krakenex.API()
        self._k.load_key('kraken.key')

        self._ledgerQueryOptions = {'ofs':0}
        if(not ledgerConfig is None):
            self._ledgerQueryOptions.update( ledgerConfig)
            
        _, self._ledger = self.queryLedgers(self._ledgerQueryOptions)

    def queryLedgers(self, options):
        ledger = self._k.query_private('Ledgers',options)
        errorsPretty = ""
        if(len(ledger["error"])==0):
            ledger = ledger["result"]["ledger"]
        else:
            errorsPretty = "\n".join(ledger["error"])
            print(f'There were errors on reading Ledger API:{errorsPretty}')
        return errorsPretty, ledger
    
    def get_ledgers(self):
        count = len(self._ledger)
        currentEntries = count
        allLedgers = []
        while (currentEntries>0):

            for k,v in self._ledger.items():
                v['ledger_id']=k
                allLedgers.append(v)

            self._ledgerQueryOptions["ofs"]=count
            error, self._ledger = self.queryLedgers(self._ledgerQueryOptions)
            if(error):
                break;
            currentEntries = len(self._ledger) 
            count = count + currentEntries
            
        return allLedgers
            