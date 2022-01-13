import requests
from accounts.bitcoin import Bitcoin

bitcoin = Bitcoin()

url = "https://wallet-api.celsius.network/wallet/balance"

payload = {}
API_KEY = "API KEY"  # gotten from the app

headers = {
  'X-Cel-Partner-Token': "PARTNER TOKEN",  # gotten from Celsius email
  'X-Cel-Api-Key': API_KEY,
}


class CelsiusPortfolio:
    def __init__(self):
        self.response = requests.request("GET", url, headers=headers, data=payload)
        self.celsius_data = self.response.json()  # this spits out a list
        # print(self.response.text)  # gives data as a str
        self.celsius_assets = {}

    def amountInBTC(self):
        btcAmount = self.celsius_data["balance"]["btc"]  # json gives data as a dict
        return float(btcAmount)

    def amountInUSD(self):
        usdAmount = self.amountInBTC() * bitcoin.getBTCPrice()
        return round(usdAmount, 2)

    def getAssets(self):
        for asset, amount in self.celsius_data["balance"].items():
            if float(amount) > 0:
                self.celsius_assets[asset] = float(amount)
        return self.celsius_assets
