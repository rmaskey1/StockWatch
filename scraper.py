from bs4 import BeautifulSoup
import requests
import json

# Default header for GET requests
header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
}

def nasdaq_stock_urls():
    url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=7675' # 'limit': how many data points to show at a time, 'offset': starting point for data to be shown
    data = requests.get(url, headers=header, timeout=5).json() # Make a GET request to the NASDAQ API, which stores all stock data in JSON objects
    # print(json.dumps(data, indent=4))

    stock_urls = {}

    for stock in data["data"]["table"]["rows"]:
        symbol = stock.get("symbol")
        url = f"https://www.nasdaq.com{stock.get('url')}"
        if '^' in symbol:
            continue
        else:
            stock_urls[symbol] = url

    # with open("sample.json", "w") as outfile:
    #    outfile.write(data)
    return stock_urls

def nasdaq_news_scrape():
    return

def real_time_price(stock_code):
    url = f"https://finance.yahoo.com/quote/{stock_code}?p={stock_code}&.tsrc=fin-srch"
    html_text = requests.get(url, headers=header, timeout=5).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    try:
        current_price = soup.find("div", class_ = "My(6px) Pos(r) smartphone_Mt(6px) W(100%)").find("fin-streamer").text
        price_change = soup.find("div", class_ = "My(6px) Pos(r) smartphone_Mt(6px) W(100%)").find_all("span")[0].text
        percent_change = soup.find("div", class_ = "My(6px) Pos(r) smartphone_Mt(6px) W(100%)").find_all("span")[1].text
        return [current_price, price_change, percent_change]
    except AttributeError:
        return []
    

print(nasdaq_stock_urls())
print(real_time_price("PRIF"))