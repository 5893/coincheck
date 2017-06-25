# coding: utf-8

import mysql.connector

from src.Model.Connector import Connector


class OrderBookModel(Connector):
    """
    板情報テーブル
    """

    def __init__(self, password):
        """
        order_books テーブルがなければ作成する
        """
        super().__init__(password)
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            create_order_book_table = (
                "CREATE TABLE IF NOT EXISTS `order_books` ("
                "`id` int(11) unsigned NOT NULL AUTO_INCREMENT,"
                "`side` varchar(5) NOT NULL,"
                "`rate` int NOT NULL,"
                "`amount` double(20,13) NOT NULL,"
                "`created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                "PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8")
            cursor.execute(create_order_book_table)
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()


    def insert_book(self, book):
        """
        板情報を保存する
        :param books = {
                            'side':         string,
                            'rate':         int,
                            'amount':       double
                        }:
        :return last_row_id int:
        """
        last_row_id = -1
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor()

            add_book = ("INSERT INTO order_books "
                         "(side, rate, amount)"
                         "VALUES (%s, %s, %s)")
            data_book = (book['side'],book['rate'],book['amount'])
            cursor.execute(add_book, data_book)
            last_row_id = cursor.lastrowid

            cnx.commit()
            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        except Exception as err:
            print(err.with_traceback())
        finally:
            cnx.close()
            return last_row_id


    def select_books(self, limit):
        """
        板情報を取得する
        :return books:
        """
        select_books = ("SELECT * FROM order_books LIMIT {}".format(limit))
        return self._select(select_books)


    def select_books_between(self, start_time, end_time):
        """
        期間を指定して板情報を取得する
        :param start_time:  class datetime.datetime
        :param end_time:    class datetime.datetime
        :return books:
        """
        select_books = ("SELECT * FROM order_books "
                         "WHERE created_at BETWEEN %s AND %s")
        return self._select(select_books, (start_time, end_time))


    @staticmethod
    def format_books_for_model(books):
        """
        /api/order_books から取得したデータを
        OrderBookModelで保存できるフォーマットのリストに変換
        :param books:
        :return books_for_model:
        """
        books_for_model = []
        sides = books.keys()
        for side in sides:
            for book in books[side]:
                rate = int(float(book[0]))  # 文字列かつ小数点.0有り => int
                model = {'side': side, 'rate': rate, 'amount': float(book[1])}
                books_for_model.append(model)
        return books_for_model
