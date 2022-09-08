import requests
from bs4 import BeautifulSoup
import re


word = input()
url = input()

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.find(string=re.compile(word)))  # Find the FIRST occurrence of the key word in a paragraph
# print(soup.find_all('p', string=re.compile(word))[0].text)
# print(soup.find_all('p', text=re.compile(word))[0].text)
