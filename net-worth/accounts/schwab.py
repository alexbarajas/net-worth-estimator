# Schwab does not have an API for public use, so just insert your shares in here
# Ameritrade does not give data for international stocks or ADRs
# Alpha Vantage does not give data for international stocks

import requests

YAHOO_FINANCE_API_KEY = "API KEY"
STOCK_ENDPOINT = "https://yfapi.net/v6/finance/quote"


class SchwabPortfolio:
    def __init__(self):
        self.stock_list = {"INCLUDE YOUR PERSONAL STOCKS NOT OBTAINABLE FROM AN API AND THEIR QUANTITY"}
        self.cash = INT # LIST CASH FROM ACCOUNTS NOT OBTAINABLE FROM AN API
        self.querystring = {
            "lang": "en",
            "symbols": self.stockList(),
        }

        self.headers = {
            "x-api-key": YAHOO_FINANCE_API_KEY
        }

        self.response = requests.get(STOCK_ENDPOINT, headers=self.headers, params=self.querystring)
        self.stock_data = self.response.json()

    def stockList(self):
        stocks = ""
        for stock in self.stock_list.keys():
            stocks += stock + ","
        stocks = stocks.rstrip(",")
        return stocks

    def schwabTotal(self):
        schwabAmount = self.cash
        for _ in range(len(self.stock_list)):
            symbol = self.stock_data["quoteResponse"]["result"][_]["symbol"]
            symbol_value = self.stock_list[symbol] * self.stock_data["quoteResponse"]["result"][_]["regularMarketPrice"]
            schwabAmount += symbol_value
        return schwabAmount

