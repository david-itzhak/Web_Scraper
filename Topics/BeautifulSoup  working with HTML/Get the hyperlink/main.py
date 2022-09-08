import requests
from bs4 import BeautifulSoup

index = int(input())
url = input()

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
a_tage_list = soup.findAll('a', href=True)
for a_tage in a_tage_list:
    if f'#act{index}' in a_tage['href']:
        print(a_tage['href'])
