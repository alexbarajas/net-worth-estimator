import requests
from accounts.crypto import Crypto

cryptocurrency = Crypto()

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

    def amountInCrypto(self, crypto):
        cryptoAmount = self.celsius_data["balance"][crypto]  # json gives data as a dict
        return float(cryptoAmount)

    def amountInUSD(self, crypto):
        usdAmount = self.amountInCrypto(crypto) * cryptocurrency.getCryptoPrice(crypto)
        return round(usdAmount, 2)

    def getAssets(self):
        for asset, amount in self.celsius_data["balance"].items():
            if float(amount) > 0:
                self.celsius_assets[asset.upper()] = float(amount)
        return self.celsius_assets

    def amountAssets(self):
        celsiusAssetAmount = 0
        for asset, amount in self.getAssets().items():
            celsiusAssetAmount += amount * Crypto().getCryptoPrice(asset)
        return celsiusAssetAmount


# print(CelsiusPortfolio().amountInCrypto("btc"))
# print(CelsiusPortfolio().amountInUSD("btc"))
# print(CelsiusPortfolio().getAssets())
# print(CelsiusPortfolio().amountAssets())
