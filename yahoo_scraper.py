from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

user_agent = {'User-Agent': 'Mozilla/5.0'}

def get_links():
    html_text = requests.get('https://finance.yahoo.com/topic/earnings',headers=user_agent).text
    soup = BeautifulSoup(html_text, 'html.parser')

    layer = soup.find('div', id = "Fin-Stream").find('ul').find_all('h3')
    #print(layer)
    links = []
    for news in layer:
        links.append(f"https://finance.yahoo.com/{news.find('a', href=True)['href']}")
    return links

def get_text(index):
    link = get_links()[index]
    
    html_text = requests.get(link, headers=user_agent).text
    soup = BeautifulSoup(html_text, 'html.parser')

    article = soup.find('article', role = "article").text
    print(article)


# main
links = get_links()
print(*links, sep="\n")
