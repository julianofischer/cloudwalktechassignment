from db.query import get_receipts, get_sales
from api.conversations import Conversation, get_conversation_info, send_message
from api.telecomm import check_chip_status
from api.logistics import track
from .msg_templates import generate_receipt_msg, generate_connection_msg, generate_delivery_forecast_msg

solutions = {}


def __load_module__():
    """ Load solutions methods to a global 'solutions' var (take advantage of first-class functions).
    :return: None
    """
    global solutions
    solutions = {'bank account receipt problem': check_receipt,
                 'connection problem': check_connection,
                 'late delivery': check_late_delivery,
                 'check delivery address': check_delivery_address,
                 'delivery forecast': check_delivery_forecast,
                 }


def solve(conversation_id: str):
    conversation = get_conversation_info(conversation_id)
    _solve(conversation)


def _solve(conversation: Conversation):
    """ Calls a solution based upon on the classification of a conversation
    :param conversation: a Conversation object
    :return: None. Maybe the message?
    """
    msg = solutions[conversation.subject](conversation.merchant_id)
    print(f'Sending message to conversation: {conversation.id} - \n |||{msg}|||')
    send_message(msg, conversation.id)


# 'bank account receipt problem'
def check_receipt(merchant_id):
    """ Run the solution for the bank account receipt problem
    :param merchant_id: the merchant id
    :return: a message which shall be sent to the merchant
    """
    receipts = get_receipts(merchant_id)
    # assumption: there are a ordered list of merchant receipts and the problem
    # is related to the last one.
    receipt = receipts[-1]
    msg = generate_receipt_msg(receipt)
    return msg


# 'connection problem'
def check_connection(merchant_id):
    """ Run the solution for the 'connection problem'
    :param merchant_id: the merchant id
    :return: a message which shall be sent to the merchant
    """
    sales = get_sales(merchant_id)
    chips = [c[2] for c in sales]
    status = []
    for chip in chips:
        status.append(check_chip_status(chip))
    return generate_connection_msg(status)


# 'late delivery'
def check_late_delivery(merchant_id):
    """ Run the solution for the 'late delivery' problem
    :param merchant_id: the merchant id
    :return: a message which shall be sent to the merchant
    """
    return check_delivery_forecast(merchant_id)


# 'check delivery address'
def check_delivery_address(merchant_id):
    """ Run the solution for the 'check delivery address' problem
    :param merchant_id: the merchant id
    :return: a message which shall be sent to the merchant
    """
    # assumption: although the subject is 'check delivery address', the chat message
    # is asking for the delivery forecast. I'm assuming that the AI is classifying
    # messages asking for delivery forecast as 'check delivery address'
    return check_delivery_forecast(merchant_id)


# 'delivery forecast'
def check_delivery_forecast(merchant_id):
    """ Run the solution for the 'delivery forecast' problem
    :param merchant_id: the merchant id
    :return: a message which shall be sent to the merchant
    """
    sales = get_sales(merchant_id)
    print(sales)
    # assumption: there are a ordered list of merchant receipts and the problem
    # is related to the last one.
    sale_id = str(sales[-1][0])
    track_info = track(sale_id)
    # zip_code = int(track_info['destination_zip_code'])
    # address_info = get_address(zip_code)
    # The chat message asks for 'where the machine will be delivered?', however, I'm unable to query
    # the zip code 60811340 using the logistics API. So, I'm assuming that the text should be
    # '*when* the machine will be delivered?'.
    print(track_info)
    return generate_delivery_forecast_msg(track_info)


# Run __load_module to load solution functions to de 'solutions' global variable.
__load_module__()
# conversation = get_conversation_info('754893')
# print(conversation)
# solve(conversation)
# print(check_connection('530364'))
# print(check_delivery_forecast('849583'))
# print(check_late_delivery('384923'))
# print(check_delivery_address('395023'))
