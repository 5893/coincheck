# coding: utf-8

from src.CoinCheckBase import CoinCheckBase


class PublicOrder(CoinCheckBase):

    def get_ticker(self):
        """
        各種最新情報を簡易に取得することができます。
        :return:
        {
          "last": 27390,            last 最後の取引の価格
          "bid": 26900,             bid 現在の買い注文の最高価格
          "ask": 27390,             ask 現在の売り注文の最安価格
          "high": 27659,            high 24時間での最高取引価格
          "low": 26400,             low 24時間での最安取引価格
          "volume": "50.29627103",  volume 24時間での取引量
          "timestamp": 1423377841   timestamp 現在の時刻
        }
        """
        url = "{}/api/ticker".format(self.uri)
        return self._request_to_coincheck('GET', url=url)


    def get_trades(self):
        """
        最新の取引履歴を取得できます。
        :return:
        [
          {
            "id": 82,
            "amount": "0.28391",
            "rate": 35400,
            "order_type": "sell",
            "created_at": "2015-01-10T05:55:38.000Z"
          },
          {
            "id": 81,
            "amount": "0.1",
            "rate": 36120,
            "order_type": "buy",
            "created_at": "2015-01-09T15:25:13.000Z"
          }
        ]
        """
        url = "{}/api/trades".format(self.uri)
        return self._request_to_coincheck('GET', url=url)


    def get_order_books(self):
        """
        板情報を取得できます。
        :return:
        asks 売り注文の情報
        bids 買い注文の情報
        {
          "asks": [
            [
              27330,
              "2.25"
            ],
            [
              27340,
              "0.45"
            ]
          ],
          "bids": [
            [
              27240,
              "1.1543"
            ],
            [
              26800,
              "1.2226"
            ]
          ]
        }
        """
        url = "{}/api/order_books".format(self.uri)
        return self._request_to_coincheck('GET', url=url)


    def get_rate(self, order_type, pair="btc_jpy", amount=0, price=0):
        """
        取引所の注文を元にレートを算出します。
        :param order_type:  *order_type 注文のタイプ（"sell" or "buy"）
        :param pair:        *pair 取引ペア。現在は "btc_jpy" のみです。
        :param amount:      amount 注文での量。（例）0.1
        :param price:       price 注文での金額。（例）28000
        :return:
        {
          "success": true,
          "rate": 60000,    rate 注文のレート
          "price": 60000,   price 注文の金額
          "amount": 1       amount 注文の量
        }
        """
        url = "{}/api/exchange/orders/rate?order_type={}&pair={}"\
                .format(self.uri, order_type, pair)
        param = ""
        if amount > 0:
            param += "&amount={}".format(amount)
        if price > 0:
            param += "&price={}".format(price)
        url_with_param = "{url}{param}".format(url=url, param=param)
        return self._request_to_coincheck('GET', url=url_with_param)


    def get_rate_pair(self, pair="btc_jpy"):
        """
        販売所のレートを取得します。
        :param pair:    *pair 通貨ペア
        ( "btc_jpy" "eth_jpy" "etc_jpy" "dao_jpy" "lsk_jpy" "fct_jpy" "xmr_jpy" "rep_jpy"
          "xrp_jpy" "zec_jpy" "xem_jpy" "ltc_jpy" "dash_jpy" "eth_btc" "etc_btc" "lsk_btc"
          "fct_btc" "xmr_btc" "rep_btc" "xrp_btc" "zec_btc" "xem_btc" "ltc_btc" "dash_btc" )
        :return:
        {
          "rate": "60000"
        }
        """
        url = "{}/api/rate/{}".format(self.uri, pair)
        return self._request_to_coincheck('GET', url=url)
