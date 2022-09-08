import requests
from bs4 import BeautifulSoup

subtitle_index = int(input())
url = input()
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
h2_list = soup.findAll('h2')
print(h2_list[subtitle_index].text)
