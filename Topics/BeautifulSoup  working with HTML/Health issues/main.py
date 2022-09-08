import requests
from bs4 import BeautifulSoup

letter = 'S'
url = input()

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
a_tag_list = soup.findAll('a')
filtered_a_tag_list = [*filter(lambda x: x.text.startswith(letter) and len(x.text) > 1 and ("topics" in x['href'] or "entity" in x['href'])
                               , a_tag_list)]
titles_list = [*map(lambda x: x.text, filtered_a_tag_list)]
print(titles_list)
