from abc import abstractproperty
import krakenex

from pipe import *
from decimal import Decimal as D
import pprint
import collections

DEBUG = False
class AvailableBalance(object):
    def __init__(self, *args):
       
        k = krakenex.API()
        k.load_key('kraken.key')

        self.__balance = k.query_private('Balance')
        market = k.query_public('Assets')
        self.__assetPairs = k.query_public('AssetPairs')
        self.__orders = k.query_private('OpenOrders')
        
        self._is_error(market)
        self._is_error(self.__balance)
        self._is_error(self.__orders)
        self._is_error(self.__assetPairs)
        
        self.__market = self.prepareAssets(market)
        self.__availableBalaces = {}
        self.__get_available_balances()

    def prepareAssets(self, market):
        market = market["result"]
        assets= []
        for k,v in market.items():
            v["name"]=k
            assets.append(v)
        return assets
            
    def _is_error(self,obj):
    
        if(len(obj["error"])>0):
            print(obj["error"])
            exit
    
    def __get_available_balances(self):

        balance = self.__balance['result']
        orders = self.__orders['result']
        assetPairs = self.__assetPairs["result"]

        pairs = list([assetPairs[x] for x in assetPairs] \
            | select(lambda x: [x["altname"],x["wsname"]]))


        newbalance = dict()
        for currency in balance:
            # remove first symbol ('Z' or 'X'), but not for GNO or DASH
            newname = currency[0:] if len(currency) == 4 and currency != "DASH" else currency
            newbalance[newname] = D(balance[currency]) # type(balance[currency]) == str
        balance = newbalance

        for _, o in orders['open'].items():
            # remaining volume in base currency
            volume = D(o['vol']) - D(o['vol_exec'])

            # extract for less typing
            descr = o['descr']

            # order price
            price = D(descr['price'])

            pair = descr['pair']
            base = list(pairs | where(lambda x: pair in x[0]) | select(lambda x: x[1].split('/')[0]))[0]
            quote = list(pairs | where(lambda x: pair in x[0]) | select(lambda x: x[1].split('/')[1]))[0]
            
            altnameQuote = list(self.__market | where(lambda x: x["altname"] == quote) | select(lambda x: x["name"]))[0]
            altnameBase = list(self.__market | where(lambda x: x["altname"] == base) | select(lambda x: x["name"]))[0]

            type_ = descr['type']
            if type_ == 'buy':
                # buying for quote - reduce quote balance
                balance[altnameQuote] -= volume * price
            elif type_ == 'sell':
                # selling base - reduce base balance
                balance[altnameBase] -= volume

            self.__availableBalaces = balance.copy()
            
    def get_avalailable_balances(self):
        orderedBalance = collections.OrderedDict(sorted(self.__availableBalaces.items()))
        if DEBUG:
            for k, v in orderedBalance.items():
                # convert to string for printing
                if v == D('0') or v < 0.00001:
                    #s = '0'
                    continue
                else:
                    s = str(v)
                # remove trailing zeros (remnant of being decimal)
                s = s.rstrip('0').rstrip('.') if '.' in s else s
                #
                print(k, s)
        return orderedBalance        
        