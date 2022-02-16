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
        self.ameritrade_assets = {}

    def accountTotals(self):
        ameritradeAmount = 0
        for account in range(len(self.ameritrade_data)):
            ameritradeAmount += self.ameritrade_data[account]["securitiesAccount"]["currentBalances"][
                "liquidationValue"]
        return ameritradeAmount

    def getAssets(self):
        for account in range(len(self.ameritrade_data)):
            for position in range(len(self.ameritrade_data[account]["securitiesAccount"]["positions"])):
                if self.ameritrade_data[account]["securitiesAccount"]["positions"][position]["instrument"][
                    "assetType"] == "EQUITY":
                    data = self.ameritrade_data[account]["securitiesAccount"]["positions"][position]
                    self.ameritrade_assets[data["instrument"]["symbol"]] = self.ameritrade_assets.get(
                        data["instrument"]["symbol"], 0) + data["marketValue"]
        return self.ameritrade_assets

# print(AmeritradePortfolio().accountTotals())  # make the values add up to one value in the class, and then return that value, and put it in the dictionary with Celsius


# print(AmeritradePortfolio().getAssets())  # get a hashmap of the assets in your ameritrade accounts
