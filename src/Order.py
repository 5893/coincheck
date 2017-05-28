# coding: utf-8

import urllib.parse
from datetime import datetime
import requests
import hmac
import hashlib

class Order:

    uri = "https://coincheck.com"
    api_key = ""
    secret_key = ""


    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key


    def get_my_transactions(self):
        url = self.uri + "/api/exchange/orders/transactions"
        return self.request_to_coincheck(url=url)


    def request_to_coincheck(self, url, body={}):
        nonce = str(int(datetime.now().timestamp()))
        signature = self.create_signature(nonce=nonce, url=url, body=urllib.parse.urlencode(body))
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-NONCE": nonce,
            "ACCESS-SIGNATURE": signature
        }
        return requests.get(url=url, headers=headers).json()


    def create_signature(self, nonce, url, body):
        message = "{}{}{}".format(nonce, url, body)
        print(message)
        return hmac.new(bytes(self.secret_key, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256).hexdigest()


if __name__ == '__main__':
    api_key = "API_KEY"
    secret_key = "API_SECRET"
    trade_logger = Order(api_key, secret_key)
