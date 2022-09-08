import requests

from bs4 import BeautifulSoup

print(BeautifulSoup(requests.get(input()).content, 'html.parser').find('h1').text)
