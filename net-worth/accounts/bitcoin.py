import requests
from bs4 import BeautifulSoup


class Bitcoin:
    def __init__(self):
        pass

    def getBTCPrice(self):
        url = "https://www.google.com/search?q=bitcoin+price"
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, "html.parser")
        btcPrice = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        price = btcPrice.split(" ")[0].replace(",", "")
        return float(price)
