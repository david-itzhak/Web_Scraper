import requests
from bs4 import BeautifulSoup
import string


def get_user_input() -> tuple:
    pages_number = int(input())
    article_type = input()
    return pages_number, article_type


def send_request(url: str) -> requests.Response:
    response: requests.Response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response:
        return response
    else:
        print(f'The URL returned {response.status_code}!')
        return None


def is_news(article):
    span_type = article.find('span', {'class': 'c-meta__type'})
    return span_type and span_type.text == 'News'


def extract_news_links(content: str) -> list[str]:
    soup = BeautifulSoup(content, 'html.parser')
    try:
        article_list = soup.find_all('article')
        a_tag_list = []
        article_list = [*filter(lambda article: is_news(article), article_list)]
        for div in article_list:
            a_tag = div.find('a', {'data-track-action': 'view article'})
            a_tag_list.append(a_tag)
        if not a_tag_list:
            print('News links not found')
            return None
        return ['https://www.nature.com' + a_tag['href'] for a_tag in a_tag_list]
    except (KeyError, AttributeError, TypeError):
        print('Error occurred!')
        return None


def save_content_to_file(file_name, content):
    try:
        with open(file_name, 'wb') as new_file:
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


def save_news_text_by_links(news_links):
    saved_articles = []
    for link in news_links:
        response = send_request(link)
        extract_text(response.content)
        title, content = extract_text(response.content)
        title = title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
        file_name = save_content_to_file(title + '.txt', content.encode())
        saved_articles.append(file_name)
    return saved_articles


def main():
    pages_number, article_type = get_user_input()
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    news_links: list = []
    for page_n in range(1, pages_number + 1):
        response: requests.Response = send_request(url)
        next_news_links: list = extract_news_links(response.content)
        news_links += next_news_links
    saved_articles = save_news_text_by_links(news_links)
    print('Saved articles: ' + str(saved_articles))


if __name__ == '__main__':
    main()

