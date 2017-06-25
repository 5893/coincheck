# coding: utf-8

import urllib.parse
from datetime import datetime
import requests
import hmac
import hashlib

class CoinCheckBase:

    uri = "https://coincheck.com"
    _api_key = ""
    _secret_key = ""


    def __init__(self, api_key, secret_key):
        self._api_key = api_key
        self._secret_key = secret_key


    def _request_to_coincheck(self, method, url, data={}):
        nonce = str(int(datetime.now().timestamp()))
        signature = self._create_signature(nonce=nonce, url=url, body=urllib.parse.urlencode(data))
        headers = {
            "ACCESS-KEY": self._api_key,
            "ACCESS-NONCE": nonce,
            "ACCESS-SIGNATURE": signature
        }
        if method == 'GET':
            response = requests.get(url=url, headers=headers)
        elif method == 'POST':
            response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"status": 404, "message": "Not Found"}
        elif response.status_code == 500:
            return {"status": 500, "message": "Internal Server Error"}


    def _create_signature(self, nonce, url, body):
        message = "{}{}{}".format(nonce, url, body)
        return hmac.new(bytes(self._secret_key, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256).hexdigest()


if __name__ == '__main__':
    api_key = "API_KEY"
    secret_key = "API_SECRET"
    trade_logger = CoinCheckBase(api_key, secret_key)