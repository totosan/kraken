from  os import name, path
from io import FileIO
from time import sleep
from datetime import datetime
import json

from pipe import sort
import utils
import AvailableBalances
from Ledger import Ledger 
import Orders
import Trades

def main():
    av = AvailableBalances.AvailableBalance()
    bal = av.get_avalailable_balances()
    
    orderstate = Orders.OrderState.closed
    o = Orders.Orders()
    orders = o.get_all_orders_by(orderstate)
    orderFile = open("orders.json","w")
    json.dump(orders, orderFile)
    
    print()
    print(f'trades history:')
    print("-------------------")
    if(path.exists("trades.json")):
        file = open("trades.json","r")
        trades = json.load(file)
    else:
        th = Trades.TradeHistroy()
        trades = th.get_tradesHistory()
        trades.sort(key=lambda x: x.get('time'))
        print(f'There {len(trades)} trades in history')
        full, rest = divmod(len(trades) , 50)
        pages = full + rest
        print(f'Fetched {pages} pages')
        #for v in trades:
        #    time = datetime.utcfromtimestamp(v["time"]).strftime('%Y-%m-%dT%H:%M:%SZ')
        #    print(f'{v}')
        file = open("trades.json","w")
        json.dump(trades,file)
        print("Wait 10s for decharge rate limits..")
        sleep(10)

    print(f'ledger entries:')
    print("-------------------")
    ledger = Ledger({'asset':"ADA"})
    ls = ledger.get_ledgers()
    ls.sort(key=lambda x: x.get('time'))
    ledgerFile =  open("ledgers.json","w")
    json.dump(ls,ledgerFile)
    for v in ls:
        if(v["type"] != "rollover"):
            time = utils.posix2DateTime(v["time"])
            print(f'{time} {v["ledger_id"][:6]} -> {v["refid"]} [ {v["type"]} {v["asset"]} {v["amount"]}]')
if __name__ == '__main__':
    main()
    