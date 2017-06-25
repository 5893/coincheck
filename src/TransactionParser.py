# coding: utf-8

class TransactionParser:

    @staticmethod
    def get_rate_average(transactions):
        sum_rate = sum([float(x["rate"]) for x in transactions])
        return sum_rate / len(transactions)


    @staticmethod
    def get_rate_average_on_sell(transactions):
        sell_rates = [float(x["rate"]) for x in transactions if x["side"] == "sell"]
        return sum(sell_rates) / len(sell_rates)


    @staticmethod
    def get_rate_average_on_buy(transactions):
        buy_rates = [float(x["rate"]) for x in transactions if x["side"] == "buy"]
        return sum(buy_rates) / len(buy_rates)


    @staticmethod
    def get_sales(transactions):
        return sum([float(x["rate"]) * (-1)*float(x["funds"]["btc"]) for x in transactions if x["side"] == "sell"])


    @staticmethod
    def get_purchase(transactions):
        return sum([float(x["rate"]) * float(x["funds"]["btc"]) for x in transactions if x["side"] == "buy"])


    @staticmethod
    def get_gain(transactions):
        return TransactionParser.get_sales(transactions) - TransactionParser.get_purchase(transactions)
