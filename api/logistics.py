import requests

API_URL = 'https://logistics-api-dot-active-thunder-329100.rj.r.appspot.com'
TRACK_ENDPOINT = 'tracking'
ZIPCODE_ENDPOINT = 'zip_code'


def track(id_sale):
    headers = {'authorization': 'teste'}
    data = {"id_sale": id_sale}
    url = f'{API_URL}/{TRACK_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())


def get_address(zip_code):
    headers = {'authorization': 'teste'}
    data = {"zip_code": zip_code}
    url = f'{API_URL}/{ZIPCODE_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())


#track("123456")
#get_address("31160550")
