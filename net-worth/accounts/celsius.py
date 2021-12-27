import requests

url = "https://wallet-api.celsius.network/wallet/BTC/balance"

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
        # print(response.text)  # gives data as a str

    def amountInBTC(self):
        btcAmount = self.celsius_data["amount"]  # json gives data as a dict
        return btcAmount

    def amountInUSD(self):
        usdAmount = self.celsius_data["amount_in_usd"]
        return round(float(usdAmount), 2)
