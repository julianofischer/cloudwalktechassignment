import requests

API_URL = 'https://chats-api-dot-active-thunder-329100.rj.r.appspot.com'
CONVERSATIONS_ENDPOINT = 'conversations'
CONVERSATION_INFO_ENDPOINT = 'conversation_info'
SEND_MESSAGE_ENDPOINT = 'send_message'


def get_conversations():
    headers = {'authorization': 'teste'}
    url = f'{API_URL}/{CONVERSATIONS_ENDPOINT}'
    response = requests.post(url, headers=headers)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())


def get_conversation_info(conversation_id):
    headers = {'authorization': 'teste'}
    data = {"conversation_id": conversation_id}
    url = f'{API_URL}/{CONVERSATION_INFO_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())


def send_message(conversation_id, msg):
    headers = {'authorization': 'teste'}
    data = {'conversation_id': conversation_id,
            'message': msg}
    url = f'{API_URL}/{SEND_MESSAGE_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())

#get_conversations()
#get_conversation_info("754893")
#send_message("754893", "Test, test")