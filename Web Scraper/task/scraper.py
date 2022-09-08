import requests


def get_url_from_user_input():
    while (url := input('Input the URL:\n')) == '':
        print('Empty input\n')
    print()
    return url


def send_request(url):
    response = requests.get(url)
    if response.status_code != 200 \
            or 'json' not in response.headers.get('content-type') \
            or 'content' not in response.json():
        print('Invalid quote resource!')
        return None
    return response


def get_quote(url):
    response = send_request(url)
    if response:
        quote = response.json().get('content')
        return quote
    else:
        return None


def main():
    url: str = get_url_from_user_input()
    quote = get_quote(url)
    if quote:
        print(quote)


if __name__ == '__main__':
    main()

