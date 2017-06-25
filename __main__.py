# coding: utf-8

import sys

from src.Model.PublicTradeModel import PublicTradeModel
from src.Order import Order
from src.PublicOrder import PublicOrder
from src.TransactionParser import TransactionParser


def main(key, secret, mysql_pass):
    # order_test(key, secret)
    # public_order_test(key, secret)
    public_trade_model_test(mysql_pass)


def public_trade_model_test(password):
    p_trade_model = PublicTradeModel(password)

    result = p_trade_model.select_trades(10)
    print(result)


def public_order_test(key, secret):
    p_order = PublicOrder(key, secret)
    # ticker
    result = p_order.get_ticker()
    for key in result.keys():
        print("{key} = {value}".format(key=key.ljust(10), value=result[key]))
    # trades
    result = p_order.get_trades()
    print("{} = {}".format("trade len".ljust(10), len(result)))
    for trade in result:
        for key in trade.keys():
            print("{key} = {value}".format(key=key.ljust(10), value=trade[key]))


def order_test(key, secret):
    order = Order(key, secret)
    result = order.get_my_transactions()

    parser = TransactionParser()

    rate_average = parser.get_rate_average(result["transactions"])
    print("rate average my transactions = {}".format(rate_average))

    rate_average_on_sell = parser.get_rate_average_on_sell(result["transactions"])
    print("rate average on sell = {}".format(rate_average_on_sell))

    rate_average_on_buy = parser.get_rate_average_on_buy(result["transactions"])
    print("rate average on buy  = {}".format(rate_average_on_buy))

    sales = parser.get_sales(result["transactions"])
    print("{} = {} JPY".format("sales".ljust(15), sales))

    purchase = parser.get_purchase(result["transactions"])
    print("{} = {} JPY".format("purchase".ljust(15), purchase))

    gain = parser.get_gain(result["transactions"])
    print("{} = {} JPY".format("current gain".ljust(15), gain))

# CoinCheck の transactions エンドポイントは 25個分までしか取得ができない (limit指定しないと50取得するけど...)


if __name__ == '__main__':
    # sys.argv[1] => api access key
    # sys.argv[2] => api secret key
    # sys.argv[3] => mysql password
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
