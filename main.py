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
    
    closedOrders = Orders.ClosedOrders()
    openedOrders = Orders.OpendOrders()
    closed = utils.loadJson(closedOrders.get_query_results, "ordersClosed")
    opened = utils.loadJson(openedOrders.get_query_results, "ordersOpen")
    if(False):
        orderstate = Orders.OrderState.closed
        closedOrders = Orders.ClosedOrders()
        closed = closedOrders.get_query_results()
        openedOrders = Orders.OpendOrders()
        sleep(5)
        opened = openedOrders.get_query_results()
        orders = []
        [orders.append(o) for o in closed]
        [orders.append(o) for o in opened]
        orderFile = open("orders.json","w")
        json.dump(orders, orderFile)
    
    print()
    print(f'trades history:')
    print("-------------------")

    th = Trades.TradeHistroy()
    trades = utils.loadJson(th.get_tradesHistory,"trades",{True,'time'})

    print(f'ledger entries:')
    print("-------------------")
    ledger = Ledger({'asset':"ADA"})
    ls = utils.loadJson(ledger.get_ledgers,"ledgers",{True,'time'})
    for v in ls:
        if(v["type"] != "rollover"):
            time = utils.posix2DateTime(v["time"])
            print(f'{time} {v["ledger_id"][:6]} -> {v["refid"]} [ {v["type"]} {v["asset"]} {v["amount"]}]')
if __name__ == '__main__':
    main()
    