from bs4 import BeautifulSoup
import requests
import json

# Header to gain access to NASDAQ API
header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
}

url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=7675' # 'limit': how many data points to show at a time, 'offset': starting point for data to be shown
data = requests.get(url, headers=header, timeout=5).json() # Make a GET request to the NASDAQ API, which stores all stock data in JSON objects


for key, value in data.items():
    symbol = ""
    if key == "symbol":
        symbol = value[key]
    print(symbol)

# with open("sample.json", "w") as outfile:
#    outfile.write(data)

url_prefix = 'https://www.nasdaq.com'
