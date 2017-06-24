# coding: utf-8

class TransactionParser:

    def __init__(self):
        pass


    def get_rate_average(self, transactions):
        sum_rate = sum([float(x["rate"]) for x in transactions])
        return sum_rate / len(transactions)


    def get_rate_average_on_sell(self, transactions):
        sell_rates = [float(x["rate"]) for x in transactions if x["side"] == "sell"]
        return sum(sell_rates) / len(sell_rates)


    def get_rate_average_on_buy(self, transactions):
        buy_rates = [float(x["rate"]) for x in transactions if x["side"] == "buy"]
        return sum(buy_rates) / len(buy_rates)


    def get_sales(self, transactions):
        return sum([float(x["rate"]) * (-1)*float(x["funds"]["btc"]) for x in transactions if x["side"] == "sell"])


    def get_purchase(self, transactions):
        return sum([float(x["rate"]) * float(x["funds"]["btc"]) for x in transactions if x["side"] == "buy"])


    def get_gain(self, transactions):
        return self.get_sales(transactions) - self.get_purchase(transactions)
