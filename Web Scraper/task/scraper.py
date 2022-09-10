import requests


def get_url_from_user_input():
    while (url := input('Input the URL:\n')) == '':
        print('Empty input\n')
    print()
    return url


def send_request(url: str) -> requests.Response:
    response: requests.Response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response.status_code != 200:
        print(f'The URL returned {response.status_code}!')
        return None
    return response


def save_content_to_file(file_name, content):
    with open(file_name, 'wb') as new_file:
        new_file.write(content)
        print('Content saved.')


def main():
    file_name = 'source.html'
    url: str = get_url_from_user_input()
    response: requests.Response = send_request(url)
    if response:
        save_content_to_file(file_name, response.content)


if __name__ == '__main__':
    main()

