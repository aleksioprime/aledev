import requests


def get_info_for_number(number: int):
    api_url = f'http://numbersapi.com/{number}'
    response = requests.get(api_url)

    if response.status_code == 200:
        print(response.text)
    else:
        print(response.status_code)


if '__main__' == __name__:
    print(get_info_for_number(43))
