# coding: utf-8

import mysql.connector

from src.Model.Connector import Connector


class PublicTradeModel(Connector):

    def __init__(self, password):
        """
        public_trades テーブルがなければ作成する
        """
        super().__init__(password)
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            add_trade = (
                "CREATE TABLE IF NOT EXISTS `public_trades` ("
                    "`id` int unsigned NOT NULL,"
                    "`amount` double(20,13) NOT NULL,"
                    "`rate` double(20, 11) NOT NULL,"
                    "`order_type` varchar(5) NOT NULL,"
                    "`created_at` datetime NOT NULL,"
                    "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8")
            cursor.execute(add_trade)
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()


    def insert_trade(self, trade):
        """
        取引履歴を保存する
        :param trades = {
                            'id':           int,
                            'amount':       double,
                            'rate':         double,
                            'order_type':   string,
                            'created_at':   class datetime.datetime
                        }:
        :return last_row_id int:
        """
        last_row_id = -1
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            add_trade = ("INSERT INTO public_trades "
                         "(id, amount, rate, order_type, created_at)"
                         "VALUES (%s, %s, %s, %s, %s)")
            data_trade = (trade['id'],trade['amount'],trade['rate'],trade['order_type'],trade['created_at'])
            cursor.execute(add_trade, data_trade)
            last_row_id = cursor.lastrowid

            cnx.commit()
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()
            return last_row_id


    def insert_trades(self, trades):
        """
        複数の取引履歴を保存する
        :param trades = [{
                            'id':           int,
                            'amount':       double,
                            'rate':         double,
                            'order_type':   string,
                            'created_at':   class datetime.datetime
                        },]:
        :return last_row_id int:
        """
        last_row_id = -1
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            add_trade = ("INSERT INTO public_trades "
                         "(id, amount, rate, order_type, created_at)"
                         "VALUES (%s, %s, %s, %s, %s)")
            data_trade = tuple([(t['id'], t['amount'], t['rate'], t['order_type'], t['created_at']) for t in trades])
            cursor.executemany(add_trade, data_trade)
            last_row_id = cursor.lastrowid

            cnx.commit()
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()
            return last_row_id


    def select_trades(self, limit):
        """
        取引履歴を取得する
        :return trades:
        """
        select_trades = ("SELECT * FROM public_trades LIMIT {}".format(limit))
        return self._select(select_trades)


    def select_trades_between(self, start_time, end_time):
        """
        期間を指定して取引履歴を取得する
        :param start_time:  class datetime.datetime
        :param end_time:    class datetime.datetime
        :return trades:
        """
        select_trades = ("SELECT * FROM public_trades "
                         "WHERE created_at BETWEEN %s AND %s")
        return self._select(select_trades, (start_time, end_time))


    def _select(self, sql, data = ()):
        trades = []
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            cursor.execute(sql, data)
            rows = cursor.fetchall()

            for row in rows:
                trades.append(row)

            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()
            return trades

