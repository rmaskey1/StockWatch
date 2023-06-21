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

def nasdaq_news_scrape(stock_code):
    offset = 0
    news_urls = []
    while True:
        url = f"https://api.nasdaq.com/api/news/topic/articlebysymbol?q={stock_code.lower()}|stocks&offset={offset}&limit=1&fallback=false"
        data = requests.get(url, headers=header, timeout=5).json()
        if "hours" in data["data"]["rows"][0]["ago"] and int(data["data"]["rows"][0]["ago"].split()[0]) > 10:
            break
        news_urls.append(f"https://www.nasdaq.com/{data['data']['rows'][0]['url']}")
        offset = offset + 1
    return news_urls

def yahoo_news_scrape(stock_code):
    url = f"https://finance.yahoo.com/quote/{stock_code}?p={stock_code}&.tsrc=fin-srch"
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')

    layer = soup.find('ul', class_ = "My(0) P(0) Wow(bw) Ov(h)").find_all('li', class_ = "js-stream-content Pos(r)")
    print(*layer, sep="\n")
    news_urls = []
    for news in layer:
        print(news.find("div", class_ = "C(#959595) Fz(11px) D(ib) Mb(6px)"))
        if "hours" in news.find_all("span")[1].text and int(news.find_all("span")[1].text.split()[0]) > 10:
            break
        news_urls.append(f"https://finance.yahoo.com/{news.find('a', href=True)['href']}")
    return news_urls

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
    

# print(nasdaq_stock_urls())
print(real_time_price("AAPL"))
#print(nasdaq_news_scrape("AAPL"))
#print(yahoo_news_scrape("AAPL"))