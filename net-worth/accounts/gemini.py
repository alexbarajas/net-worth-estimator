import requests
import time
import base64
import json
import hmac
import hashlib
from .bitcoin import Bitcoin

bitcoin = Bitcoin()

base_url = "https://api.gemini.com"
endpoint = "/v1/balances"  # to get the account balances
# endpoint = "/v1/balances/earn"  # to get the earn balances
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

    def btcAmountInBTC(self):
        btcQuantityBTC = self.gemini_data[1]["available"]
        btcAmountBTC = float(btcQuantityBTC)
        return btcAmountBTC

    def btcAmountInUSD(self):
        btcQuantityUSD = self.gemini_data[1]["available"]
        btcAmountUSD = float(btcQuantityUSD) * bitcoin.getBTCPrice()
        return btcAmountUSD

    def cashAmountInUSD(self):
        cashAmountUSD = float(self.gemini_data[0]["available"])
        return cashAmountUSD
