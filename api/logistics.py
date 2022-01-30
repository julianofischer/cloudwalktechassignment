import requests

API_URL = 'https://logistics-api-dot-active-thunder-329100.rj.r.appspot.com'
TRACK_ENDPOINT = 'tracking'
ZIPCODE_ENDPOINT = 'zip_code'


def track(id_sale):
    # only strings
    id_sale = str(id_sale)
    headers = {'authorization': 'teste'}
    data = {"id_sale": id_sale}
    url = f'{API_URL}/{TRACK_ENDPOINT}'
    print(url)
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def get_address(zip_code):
    headers = {'authorization': 'teste'}
    data = {"zip_code": zip_code}
    url = f'{API_URL}/{ZIPCODE_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# print(track('123458'))
# print(get_address(60811340))
