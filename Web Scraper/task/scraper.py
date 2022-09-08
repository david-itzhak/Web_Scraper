import bs4 as bs4
import requests
from bs4 import BeautifulSoup


def get_url_from_user_input():
    while (url := input('Input the URL:\n')) == '':
        print('Empty input\n')
    print()
    return url


def send_request(url: str) -> requests.Response:
    response: requests.Response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response.status_code != 200:
        print('Invalid response!')
        return None
    return response


def get_title_description(response: str) -> dict[str, str]:
    soup = BeautifulSoup(response, 'html.parser')
    try:
        title_description_dict: dict[str, str] = {}
        title_tag: BeautifulSoup.Tag = soup.find('h1')
        description_meta_tag: BeautifulSoup.Tag = soup.find('span', {'data-testid': 'plot-l'})
        if not title_tag or not description_meta_tag:
            print('Invalid movie page!')
            return None
        title_description_dict['title'] = title_tag.text
        title_description_dict['description'] = description_meta_tag.text
        return title_description_dict
    except (KeyError, AttributeError, TypeError):
        print('Invalid movie page!')
        return None


def main():
    url: str = get_url_from_user_input()
    response: requests.Response = send_request(url)
    if response:
        title_description_dict: dict[str, str] = get_title_description(response.content)
    if title_description_dict:
        print(title_description_dict)


if __name__ == '__main__':
    main()

