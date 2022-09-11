import requests
from bs4 import BeautifulSoup
import string
import os


def get_user_input() -> tuple:
    pages_number = int(input())
    article_type = input()
    return pages_number, article_type


def send_request(url: str) -> requests.Response:
    return requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})


def is_necessary_type(article, article_type):
    span_type = article.find('span', {'class': 'c-meta__type'})
    return span_type and span_type.text == article_type


def extract_news_links(content: str, article_type: str) -> list[str]:
    soup = BeautifulSoup(content, 'html.parser')
    try:
        article_list = soup.find_all('article')
        a_tag_list = []
        article_list = [*filter(lambda article: is_necessary_type(article, article_type), article_list)]
        for div in article_list:
            a_tag = div.find('a', {'data-track-action': 'view article'})
            a_tag_list.append(a_tag)
        if not a_tag_list:
            return None
        return ['https://www.nature.com' + a_tag['href'] for a_tag in a_tag_list]
    except (KeyError, AttributeError, TypeError):
        print('Error occurred!')
        return None


def save_content_to_file(file_name, content, page_n):
    try:
        with open(f'./Page_{page_n}/' + file_name, 'wb') as new_file:
            new_file.write(content)
            return file_name
    except(Exception):
        print('Error occurred: ' + Exception)


def extract_text(content):
    soup = BeautifulSoup(content, 'html.parser')
    meta_title = soup.find('meta', {'name': 'dc.title'})
    title = meta_title['content']
    text_elements = soup.find('div', {'class': 'c-article-body'}).find_all(('p', 'h2'))
    text = '\n'.join([el.text for el in text_elements if not el.text.startswith('\n')])
    return title, text.strip()


def save_news_text_by_links(news_links, page_n):
    os.mkdir(f'Page_{page_n}')
    saved_articles = []
    if not news_links:
        return
    for link in news_links:
        response = send_request(link)
        if response:
            extract_text(response.content)
            title, content = extract_text(response.content)
            title = title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            file_name = save_content_to_file(title + '.txt', content.encode(), page_n)
            saved_articles.append(file_name)
    return saved_articles


def main():
    pages_number, article_type = get_user_input()
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    for page_n in range(1, pages_number + 1):
        response: requests.Response = send_request(url + f'&page={page_n}')
        if response.status_code == 404:
            break
        news_links: list = extract_news_links(response.content, article_type)
        save_news_text_by_links(news_links, page_n)
    print('Saved all articles.')


if __name__ == '__main__':
    main()

