import json
from datetime import date
from accounts.celsius import CelsiusPortfolio
from accounts.ameritrade import AmeritradePortfolio
from accounts.schwab import SchwabPortfolio
from accounts.gemini import GeminiPortfolio
from accounts.bitcoin import Bitcoin
from data.plot import Plot

# set up the imported modules
celsiusPortfolio = CelsiusPortfolio()
ameritradePortfolio = AmeritradePortfolio()
schwabPortfolio = SchwabPortfolio()
geminiPortfolio = GeminiPortfolio()
cryptocurrency = Crypto()
portfolio_file = "data/portfolio_data.json"
asset_file = "data/asset_data.json"
plot = Plot(portfolio_file)
today = date.today()

def getOverallPlot():
    accounts = {
        str(today): {
            "Celsius": celsiusPortfolio.amountAssets(),
            # "Ameritrade": ameritradePortfolio.accountTotals(),
            "Schwab": schwabPortfolio.schwabTotal(),
            "Gemini": geminiPortfolio.cryptoAmountInUSD("btc") + geminiPortfolio.cashAmountInUSD()
        }
    }

    # check if the file exists
    with open(portfolio_file, "r+") as file:
        try:  # check if a file can be loaded up
            json.load(file)
        except FileNotFoundError:  # if not then make it and add to it
            json.dump([accounts], file)

    # write list to file
    with open(portfolio_file, 'r+') as data:
        json_data = json.load(data)
        if type(json_data) is dict:
            json_data = [json_data]
        if len(json_data) > 0:
            for key, values in json_data[-1].items():
                if key == str(today):  # this updates a day if it's already in the json
                    json_data[-1] = {
                        str(today): {
                            "Celsius": celsiusPortfolio.amountAssets(),
                            # "Ameritrade": ameritradePortfolio.accountTotals(),
                            "Schwab": schwabPortfolio.schwabTotal(),
                            "Gemini": geminiPortfolio.cryptoAmountInUSD("btc") + geminiPortfolio.cashAmountInUSD()
                        }
                    }
                else:  # adds a day if not in the json
                    json_data.append({
                        str(today): {
                            "Celsius": celsiusPortfolio.amountAssets(),
                            # "Ameritrade": ameritradePortfolio.accountTotals(),
                            "Schwab": schwabPortfolio.schwabTotal(),
                            "Gemini": geminiPortfolio.cryptoAmountInUSD("btc") + geminiPortfolio.cashAmountInUSD()
                        }
                    })
            data.seek(0)  # makes sure the json is properly formatted
            data.write(json.dumps(json_data))
            data.truncate()

    plot.setup_plot()


# getOverallPlot()  # makes a plot with accounts instead of individual assets


def getAssets():
    assets = {}
    try:
        with open(asset_file, "r+") as file:  # reads a file if there is one
            print("File has been read.")
            json.load(file)
    except FileNotFoundError:  # if no file then make it and add to it
        with open(asset_file, "a+") as file:
            print("File has been added.")
            json.dump([assets], file)
    except json.JSONDecodeError:  # if there is a file but it has no data add data to it
        with open(asset_file, "a+") as file:
            print("Data has been added.")
            json.dump([assets], file)

    with open(asset_file, "r+") as data:
        json_data = json.load(data)
        if type(json_data) is dict:
            json_data = [json_data]
        crypto = {}
        stocks = {}
        for asset, amount in celsiusPortfolio.getAssets().items():
            crypto[asset] = crypto.get(asset, 0) + amount
        for asset, amount in geminiPortfolio.getAssets().items():
            crypto[asset] = crypto.get(asset, 0) + amount
        for asset, amount in schwabPortfolio.getAssets().items():
            stocks[asset] = stocks.get(asset, 0) + amount
        # for asset, amount in ameritradePortfolio.getAssets().items():
        #     stocks[asset] = stocks.get(asset, 0) + amount
        json_data[-1][str(today)] = {"crypto": crypto, "stocks": stocks}
        for crypto in json_data[-1][str(today)]["crypto"]:  # do this after you add all crypto from all accounts
            json_data[-1][str(today)]["crypto"][crypto] *= cryptocurrency.getCryptoPrice(crypto)
        data.seek(0)  # makes sure the json is properly formatted
        data.write(json.dumps(json_data))
        data.truncate()


getAssets()
