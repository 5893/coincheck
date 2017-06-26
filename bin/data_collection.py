# coding: utf-8

import sys
sys.path.append('..')

from datetime import datetime as dt

from src.Model.OrderBookModel import OrderBookModel
from src.Model.PublicTradeModel import PublicTradeModel
from src.PrivateOrder import PrivateOrder
from src.PublicOrder import PublicOrder
from src.TransactionParser import TransactionParser


def main(key, secret, mysql_pass):
    get_and_save_public_trades(key, secret, mysql_pass)
    get_and_save_order_books(key, secret, mysql_pass)


def get_and_save_public_trades(key, secret, mysql_pass):
    p_order = PublicOrder(key, secret)
    pt_model = PublicTradeModel(mysql_pass)

    # request trades
    trades = p_order.get_trades()
    # print("{} = {}".format("get trade count".ljust(10), len(trades)))

    # save trades
    inserted_ids = []
    for trade in trades:
        trade['created_at'] = dt.strptime(trade['created_at'].replace('.000Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z')
        trade['amount'] = float(trade['amount'])
        inserted_id = pt_model.insert_trade(trade)
        if inserted_id > 0:
            inserted_ids.append(inserted_id)
    # print("{} = {}".format("saved count".ljust(10), len(inserted_ids)))


def get_and_save_order_books(key, secret, mysql_pass):
    p_order = PublicOrder(key, secret)
    ob_model = OrderBookModel(mysql_pass)

    books_from_api = p_order.get_order_books()
    books_for_model = ob_model.format_books_for_model(books_from_api)
    for book in books_for_model:
        # print("side: {}\trate: {}\t amount: {}".format(book['side'], book['rate'], book['amount']))
        ob_model.insert_book(book)


if __name__ == '__main__':
    # sys.argv[1] => api access key
    # sys.argv[2] => api secret key
    # sys.argv[3] => mysql password
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
