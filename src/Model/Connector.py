# coding: utf-8

import mysql.connector
from mysql.connector import errorcode

class Connector:

    _config = {}


    def __init__(self, password):
        self._config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'coincheck',
            'user': 'root',
            'password': password,
            'charset': 'utf8',
            'use_unicode': True,
            'get_warnings': True,
        }


    def _get_connector(self):
        return mysql.connector.Connect(**self._config)


    def _select(self, sql, data = ()):
        result = []
        try:
            cnx = self._get_connector()
            cursor = cnx.cursor(dictionary=True)

            cursor.execute(sql, data)
            rows = cursor.fetchall()

            for row in rows:
                result.append(row)

            cursor.close()

        except mysql.connector.Error as err:
            self._print_connector_error(err)
        finally:
            cnx.close()
            return result


    def _print_connector_error(self, err):
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
