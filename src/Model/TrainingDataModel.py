# coding: utf-8

import mysql.connector

from src.Model.OrderBookModel import OrderBookModel
from src.Model.PublicTradeModel import PublicTradeModel


class TrainingDataModel(OrderBookModel, PublicTradeModel):
    """
    学習用データ
    """

    def __init__(self, password):
        """
        学習用データテーブルがなければ作成する
        :param password:
        """
        super().__init__(password)
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            create_training_data = (
                "CREATE TABLE IF NOT EXISTS `training_data` ("
                "`id` int NOT NULL AUTO_INCREMENT,"
                "`target_rate` int NOT NULL,"
                "`asks_max_rate` int NOT NULL,"
                "`asks_min_rate` int NOT NULL,"
                "`asks_amount` double(20,13) NOT NULL,"
                "`bids_max_rate` int NOT NULL,"
                "`bids_min_rate` int NOT NULL,"
                "`bids_amount` double(20,13) NOT NULL,"
                "`target_time` datetime NOT NULL,"	        # 目的変数の日時(ここから1分間)
                "`books_time` datetime NOT NULL,"		    # 説明変数の日時(ここから1分間)
                "PRIMARY KEY (`id`),"
                "UNIQUE KEY unique_time (target_time, books_time)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8")
            cursor.execute(create_training_data)
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()


    def select_training_data(self):
        """
        学習データを取得する
        :return:
        """
        select_data = ("SELECT * FROM training_data")
        return self._select(select_data, ())


    def insert_training_data(self, data):
        """
        学習データを保存する
        :param data:
        :return:
        """
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            add_data_sql = ("INSERT INTO training_data "
                        "(target_rate, asks_max_rate, asks_min_rate, "
                        "asks_amount, bids_max_rate, bids_min_rate, bids_amount,"
                        "target_time, books_time)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            add_data_tuple = (data['target_rate'], data['asks_max_rate'],
                              data['asks_min_rate'], data['asks_amount'],
                              data['bids_max_rate'], data['bids_min_rate'],
                              data['bids_amount'], data['target_time'],
                              data['books_time'])
            cursor.execute(add_data_sql, add_data_tuple)

            cnx.commit()
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        except Exception as err:
            print(err.with_traceback())
        finally:
            cnx.close()
            return (data['target_time'], data['books_time'])

    def get_last_time(self):
        """
        最新の説明変数の対象時間を取得する
        """
        select_data = ("SELECT books_time FROM training_data ORDER BY books_time DESC LIMIT 1")
        return self._select(select_data, ())
