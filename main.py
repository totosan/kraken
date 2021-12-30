from datetime import datetime
from  os import name, path
from io import StringIO
from time import sleep
import json

import utils
from pipe import sort

from AvailableBalances import AvailableBalance
from Ledgers import Ledgers
import Orders
import Trades


def main():
    av = AvailableBalance()
    bal = av.get_avalailable_balances()
    
    if False:
        closedOrders = Orders.ClosedOrders()
        openedOrders = Orders.OpendOrders()
        closed = utils.lastState(closedOrders.get_query_results, "ordersClosed")
        opened = utils.lastState(openedOrders.get_query_results, "ordersOpen")
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
    th = Trades.TradeHistory()
    data = th.get_from_Export(startDate=utils.date2nix(datetime(2021,1,1)))
    
    print(f'ledger entries:')
    print("-------------------")
    lh = Ledgers()
    data = lh.get_from_Export(startDate=utils.date2nix(datetime(2021,1,1)))

    ledger = Ledgers({'asset':"ADA"})
    ls = utils.lastState(ledger.get_query_results,"ledgers",sorted='time')
    for v in ls:
        if(v["type"] != "rollover"):
            time = utils.posix2DateTime(v["time"])
            print(f'{time} {v["entity_id"][:6]} -> {v["refid"]} [ {v["type"]} {v["asset"]} {v["amount"]}]')


if __name__ == '__main__':
    main()
    