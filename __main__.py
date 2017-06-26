# coding: utf-8

import sys
from datetime import datetime as dt

from src.Model.OrderBookModel import OrderBookModel
from src.Model.PublicTradeModel import PublicTradeModel
from src.PrivateOrder import PrivateOrder
from src.PublicOrder import PublicOrder
from src.TransactionParser import TransactionParser


def main(key, secret, mysql_pass):
    pass


if __name__ == '__main__':
    # sys.argv[1] => api access key
    # sys.argv[2] => api secret key
    # sys.argv[3] => mysql password
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
