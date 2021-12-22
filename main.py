from os import name

from pipe import sort
import AvailableBalances
from Ledger import Ledger 
import Orders
from datetime import datetime
def main():
    av = AvailableBalances.AvailableBalance()
    print("available balances:")
    print("-------------------")
    av.display()
    
    orderstate = Orders.OrderState.open
    o = Orders.Orders()
    print()
    print(f'{orderstate} orders:')
    print("-------------------")
    o.get_all_orders_by(orderstate)
    
    print()
    print(f'ledger entries:')
    print("-------------------")
    ledger = Ledger({'asset':"ADA"})
    ls = ledger.get_ledgers()
    ls.sort(key=lambda x: x.get('time'))
    for v in ls:
        if(v["type"] != "rollover"):
            time = datetime.utcfromtimestamp(v["time"]).strftime('%Y-%m-%dT%H:%M:%SZ')
            print(f'{time} {v["ledger_id"][:6]} -> {v["refid"]} [ {v["type"]} {v["asset"]} {v["amount"]}]')
if __name__ == '__main__':
    main()
    