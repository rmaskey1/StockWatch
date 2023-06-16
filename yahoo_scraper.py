from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://finance.yahoo.com/topic/earnings').text
soup = BeautifulSoup(html_text, 'html.parser')

layer = soup.find('div', id = "Fin-Stream").find('ul').find_all('h3')
print(layer)
for news in layer:
    links = news.find_all('a', href=True)
print(links)
