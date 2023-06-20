import requests
from bs4 import BeautifulSoup

def get_links():
    user_agent = {'User-Agent':'Mozilla/5.0'}
    html_text = requests.get('https://www.wsj.com/news/markets/stocks', headers=user_agent).text
    soup = BeautifulSoup(html_text, 'html.parser')

    layer = soup.find('div', {"id":"latest-stories"}).find_all('h2')
    #print(layer)
    links = []
    for news in layer:
        links.append(news.find('a', href=True)['href'])
    return links

print(get_links())