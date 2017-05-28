# coding: utf-8

import sys
from src.Order import Order


def main(key, secret):
    order = Order(key, secret)
    result = order.get_my_transactions()
    print(result)


if __name__ == '__main__':
    # sys.argv[1] => api access key
    # sys.argv[2] => api secret key
    main(str(sys.argv[1]), str(sys.argv[2]))
