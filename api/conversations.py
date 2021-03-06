import requests

API_URL = 'https://chats-api-dot-active-thunder-329100.rj.r.appspot.com'
CONVERSATIONS_ENDPOINT = 'conversations'
CONVERSATION_INFO_ENDPOINT = 'conversation_info'
SEND_MESSAGE_ENDPOINT = 'send_message'


class ConversationMessage:
    """A class representing messages from a conversation """
    def __init__(self, idx, text, created_at):
        self.id = idx
        self.text = text
        self.created_at = created_at

    def __str__(self):
        return f'<{self.id} - {self.created_at}> - <{self.text}>'

    def __repr__(self):
        return self.__str__()


class Conversation:
    """A class representing a entire conversation with merchants"""
    def __init__(self, idx, messages, merchant_id, subject):
        self.id = idx
        self.messages = messages
        self.merchant_id = merchant_id
        self.subject = subject

    def __str__(self):
        return f'''conversation_id: {self.id}
        messages: {self.messages}
        merchant_id: {self.merchant_id}
        subject: {self.subject}'''


def get_conversations() -> list:
    """
    :return: a list of conversation ids, whose conversations are happening in the same time as the request,
    it means, a **list of the active conversation ids**.
    """
    headers = {'authorization': 'teste'}
    url = f'{API_URL}/{CONVERSATIONS_ENDPOINT}'
    response = requests.post(url, headers=headers)
    ids = [str(idx) for idx in response.json()['conversation_ids']]
    return ids


def _make_messages(msgs: list) -> list:
    """Given a list containing information about conversation messages, constructs a list of
    ConversationMessage objects
    :param msgs:  the list containing information about conversation messages
    :return: a list of ConversationMessage objects
    """
    ret = []
    for msg in msgs:
        ret.append(ConversationMessage(msg['message_id'], msg['text'], msg['created_at']))
    return ret


def get_conversation_info(conversation_id: str) -> Conversation:
    """
    :param conversation_id: the conversation unique id
    :return: returns a object of Conversation class containing conversation information:
    """
    headers = {'authorization': 'teste'}
    data = {"conversation_id": conversation_id}
    url = f'{API_URL}/{CONVERSATION_INFO_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    jsonx = response.json()
    conversation_id = jsonx['conversation_id']
    merchant_id = jsonx['merchant_id']
    subject = jsonx['subject']
    messages = _make_messages(jsonx['messages'])
    return Conversation(conversation_id, messages, merchant_id, subject)


def send_message(conversation_id, msg):
    """ Sends a message to a open conversation.
    :param conversation_id: the conversation unique id.
    :param msg: the message which will be sent to the conversation
    :return: the HTTP response code
    """
    headers = {'authorization': 'teste'}
    data = {'conversation_id': conversation_id,
            'message': msg}
    url = f'{API_URL}/{SEND_MESSAGE_ENDPOINT}'
    response = requests.post(url, json=data, headers=headers)
    return response.status_code

'''get_conversations()
print(get_conversation_info("754893"))
send_message("754893", "Test, test")
for conversation in get_conversations():
    get_conversation_info(conversation)'''
