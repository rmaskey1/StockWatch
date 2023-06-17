import requests
from bs4 import BeautifulSoup

def get_links():
    html_text = requests.get('https://www.wsj.com/news/markets/stocks').text
    soup = BeautifulSoup(html_text, 'html.parser')

    layer = soup.find_all('div', {"id":"latest-stories"})
    print(layer)
    links = []
    for news in layer:
        links.append(news.find('a', href=True)['href'])
    return links

print(get_links())