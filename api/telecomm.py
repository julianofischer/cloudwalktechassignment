import requests


API_URL = 'https://telecom-api-dot-active-thunder-329100.rj.r.appspot.com'
CHIP_STATUS_ENDPOINT = 'chip_status'


def check_chip_status(chip_id: str) -> dict:
    """ Used to check the chip status.
    :param chip_id: the chip unique ID, for instance: "CHIP37648"
    :return: a dict containing information about the chip status: {'id': 'CHIP37648', 'status': 'active',
    'description': 'OK'}
    """
    headers = {'authorization': 'teste'}
    data = {"chip_id": chip_id}
    url = f'{API_URL}/{CHIP_STATUS_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# print(check_chip_status("CHIP37648"))