import requests

client_id = "CLIENT ID"
api_key = "API KEY"
endpoint = f"https://api.tdameritrade.com/v1/accounts?fields=positions"
# the bearer_token is what goes into "refresh_token" when you go and get a new access_token
bearer_token = "BEARER TOKEN"
access_token = "ACCESS TOKEN"
headers = {  # uses the access_token after "Bearer " in the value, expires after 90 days, use this link to get new tokens: https://developer.tdameritrade.com/content/authentication-faq , last created 11/12/21
    "Authorization": "Bearer " + access_token  # Access token, this expires after 30 minutes
}


class AmeritradePortfolio:
    def __init__(self):
        self.response = requests.get(url=endpoint, headers=headers)
        self.ameritrade_data = self.response.json()  # this spits out a list

    def accountTotals(self):
        ameritradeAmount = 0
        for account in range(len(self.ameritrade_data)):
            ameritradeAmount += self.ameritrade_data[account]["securitiesAccount"]["currentBalances"]["liquidationValue"]
        return ameritradeAmount
