# coding: utf-8

from src.CoinCheckBase import CoinCheckBase


class PrivateOrder(CoinCheckBase):

    def new_market_ordr(self, order_type, amount):
        url = "{}/api/exchange/orders".format(self.uri)
        pass


    def new_limit_order(self, order_type, rate, amount):
        url = "{}/api/exchange/orders".format(self.uri)
        pass


    def get_my_transactions(self):
        url = "{}/api/exchange/orders/transactions".format(self.uri)
        return self._request_to_coincheck('GET', url=url)


if __name__ == '__main__':
    api_key = "API_KEY"
    secret_key = "API_SECRET"
    trade_logger = PrivateOrder(api_key, secret_key)
