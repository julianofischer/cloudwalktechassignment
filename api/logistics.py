import requests

API_URL = 'https://logistics-api-dot-active-thunder-329100.rj.r.appspot.com'
TRACK_ENDPOINT = 'tracking'
ZIPCODE_ENDPOINT = 'zip_code'


def track(id_sale: str) -> dict:
    """Useful to track the delivery of InfinitePay's credit card machines.
    :param id_sale: InfinitePay's sales unique id - it's a sale of credit card machine made by InfinitePay
    :return: a dict containing track info such as this: {'id': '123458', 'status':
    'In transit between distribution centers', 'delivery_forecast': '01/03/2022',
    'destination_zip_code': '60811340'}
    """
    # only strings
    headers = {'authorization': 'teste'}
    data = {"id_sale": id_sale}
    url = f'{API_URL}/{TRACK_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def get_address(zip_code: str) -> dict:
    """Given a ZIP code, give the complete address as the response.
    :param zip_code: the ZIP code
    :return: a dict containing the complete address - {'neighborhood': 'Palmares', 'ZIP_code': '31160-550',
    'city': 'Belo Horizonte', 'complement': '', 'street': 'Rua Professor Patrocínio Filho', 'state': 'MG'}
    """
    headers = {'authorization': 'teste'}
    data = {"zip_code": zip_code}
    url = f'{API_URL}/{ZIPCODE_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# print(track('123458'))
# print(get_address('31160550'))
