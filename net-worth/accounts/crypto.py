import requests


class Crypto:
    def __init__(self):
        self.coinMarketCapAPIKey = "API GOTTEN FROM COINMARKETCAP"
        self.coinMarketCapURL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        
        pass

    def getCryptoPrice(self, crypto):
        crypto = crypto
        coinMarketCapParameters = {
            "symbol": crypto
        }
        coinMarketCapHeaders = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.coinMarketCapAPIKey
        }
        response = requests.get(self.coinMarketCapURL, params=coinMarketCapParameters, headers=coinMarketCapHeaders)
        cryptoPrice = response.json()["data"][crypto.upper()]["quote"]["USD"]["price"]
        return cryptoPrice

# print(Crypto().getCryptoPrice("btc"))
# print(Crypto().getCryptoPrice("eth"))
# print(Crypto().getCryptoPrice("gusd"))
