import requests
import time
import base64
import json
import hmac
import hashlib
from accounts.crypto import Crypto

cryptocurrency = Crypto()

base_url = "https://api.gemini.com"
endpoint = "/v1/balances"  # to get the account balances
API_KEY = "API KEY"
SECRET_API = "SECRET API".encode()
NONCE = str(int(time.time() * 10000000))  # this number will always increase, and never be repeated

payload = {
    "request": endpoint,
    "nonce": NONCE
}
encoded_payload = json.dumps(payload).encode()
based64 = base64.b64encode(encoded_payload)
signature = hmac.new(SECRET_API, based64, hashlib.sha384).hexdigest()

headers = {
    "X-GEMINI-APIKEY": API_KEY,
    "X-GEMINI-PAYLOAD": based64,
    "X-GEMINI-SIGNATURE": signature
}


class GeminiPortfolio:
    def __init__(self):
        self.response = requests.post(url=base_url + endpoint, headers=headers)
        self.gemini_data = self.response.json()
        # print(self.gemini_data)
        self.gemini_assets = {}

    def cryptoAmountInCrypto(self, crypto):
        cryptoAmountCrypto = 0
        for asset in range(len(self.gemini_data)):
            if self.gemini_data[asset]["currency"] == crypto.upper():
                cryptoQuantityCrypto = self.gemini_data[asset]["amount"]
                cryptoAmountCrypto = float(cryptoQuantityCrypto)
        return cryptoAmountCrypto

    def cryptoAmountInUSD(self, crypto):
        cryptoAmountUSD = 0
        for asset in range(len(self.gemini_data)):
            if self.gemini_data[asset]["currency"] == crypto.upper():
                cryptoQuantityUSD = self.gemini_data[asset]["amount"]
                cryptoAmountUSD = float(cryptoQuantityUSD) * cryptocurrency.getCryptoPrice("btc")
        return round(cryptoAmountUSD, 2)

    def cashAmountInUSD(self):
        cashAmountUSD = 0
        for asset in range(len(self.gemini_data)):
            if self.gemini_data[asset]["currency"] == "USD":
                cashAmountUSD = float(self.gemini_data[asset]["amount"])
        return round(cashAmountUSD, 2)

    def getAssets(self):
        for i in range(len(self.gemini_data)):
            if self.gemini_data[i]["currency"] == "USD":
                continue
            else:
                self.gemini_assets[self.gemini_data[i]["currency"].upper()] = float(self.gemini_data[i]["amount"])
        return self.gemini_assets

# print(GeminiPortfolio().cryptoAmountInCrypto("btc"), "btc in btc")
# print(GeminiPortfolio().cryptoAmountInUSD("btc"), "btc in usd")
# print(GeminiPortfolio().cashAmountInUSD(), "usd in usd")
# print(GeminiPortfolio().gemini_data)
# print(GeminiPortfolio().getAssets())
