import json
from datetime import date
from accounts.celsius import CelsiusPortfolio
from accounts.ameritrade import AmeritradePortfolio
from accounts.schwab import SchwabPortfolio
from accounts.gemini import GeminiPortfolio
from accounts.bitcoin import Bitcoin

celsiusPortfolio = CelsiusPortfolio()
ameritradePortfolio = AmeritradePortfolio()
schwabPortfolio = SchwabPortfolio()
geminiPortfolio = GeminiPortfolio()
bitcoin = Bitcoin()

today = date.today()

filename = "data/portfolio_data.json"

accounts = {
    str(today): {
        "Celsius": celsiusPortfolio.amountInUSD(),
        # "Ameritrade": ameritradePortfolio.accountTotals(),
        "Schwab": schwabPortfolio.schwabTotal(),
        "Gemini": geminiPortfolio.btcAmountInUSD() + geminiPortfolio.cashAmountInUSD()
    }
}

# check if the file exists
with open(filename, "r+") as file:
    try:  # check if a file can be loaded up
        data_load = json.load(file)
    except:  # if not then make it and add to it
        json.dump([accounts], file)

# write list to file
with open(filename, 'r+') as data:
    json_data = json.load(data)
    if type(json_data) is dict:
        json_data = [json_data]
    if len(json_data) > 0:
        for key, values in json_data[-1].items():
            if key == str(today):  # this updates a day if it's already in the json
                json_data[-1] = {
                    str(today): {
                        "Celsius": celsiusPortfolio.amountInUSD(),
                        # "Ameritrade": ameritradePortfolio.accountTotals(),
                        "Schwab": schwabPortfolio.schwabTotal(),
                        "Gemini": geminiPortfolio.btcAmountInUSD() + geminiPortfolio.cashAmountInUSD()
                    }
                }
            else:  # adds a day if not in the json
                json_data.append({
                    str(today): {
                        "Celsius": celsiusPortfolio.amountInUSD(),
                        # "Ameritrade": ameritradePortfolio.accountTotals(),
                        "Schwab": schwabPortfolio.schwabTotal(),
                        "Gemini": geminiPortfolio.btcAmountInUSD() + geminiPortfolio.cashAmountInUSD()
                    }
                })
        data.seek(0)  # makes sure the json is properly formatted
        data.write(json.dumps(json_data))
        data.truncate()

