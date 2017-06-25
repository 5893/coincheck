# coding: utf-8

import sys
from datetime import datetime as dt

from src.Model.PublicTradeModel import PublicTradeModel
from src.PrivateOrder import PrivateOrder
from src.PublicOrder import PublicOrder
from src.TransactionParser import TransactionParser


def main(key, secret, mysql_pass):
    get_and_save_public_trades(key, secret, mysql_pass)


def get_and_save_public_trades(key, secret, mysql_pass):
    p_order = PublicOrder(key, secret)
    pt_model = PublicTradeModel(mysql_pass)

    # request trades
    trades = p_order.get_trades()
    print("{} = {}".format("get trade count".ljust(10), len(trades)))

    # save trades
    inserted_ids = []
    for trade in trades:
        trade['created_at'] = dt.strptime(trade['created_at'].replace('.000Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z')
        trade['amount'] = float(trade['amount'])
        inserted_id = pt_model.insert_trade(trade)
        if inserted_id > 0:
            inserted_ids.append(inserted_id)
    print("{} = {}".format("saved count".ljust(10), len(inserted_ids)))


if __name__ == '__main__':
    # sys.argv[1] => api access key
    # sys.argv[2] => api secret key
    # sys.argv[3] => mysql password
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
