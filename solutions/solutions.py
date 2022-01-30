import argparse
from db.query import get_receipts, get_sales, get_transactions
from api.conversations import Conversation, get_conversation_info
from api.telecomm import check_chip_status
from api.logistics import track, get_address
from msg_templates import generate_receipt_msg, generate_connection_msg, generate_delivery_forecast_msg

solutions = {}


def __load_module__():
    global solutions
    solutions = {'bank account receipt problem': check_receipt,
                 'connection problem': check_connection,
                 'late delivery': check_late_delivery,
                 'check delivery address': check_delivery_address,
                 'delivery forecast': check_delivery_forecast,
                 }


def solve(conversation: Conversation):
    solutions[conversation.subject](conversation.merchant_id)


# 'bank account receipt problem'
def check_receipt(merchant_id):
    receipts = get_receipts(merchant_id)
    # assumption: there are a ordered list of merchant receipts and the problem
    # is related to the last one.
    receipt = receipts[-1]
    msg = generate_receipt_msg(receipt)
    return msg


# 'connection problem'
def check_connection(merchant_id):
    sales = get_sales(merchant_id)
    chips = [c[2] for c in sales]
    status = []
    for chip in chips:
        status.append(check_chip_status(chip))
    return generate_connection_msg(status)


# 'late delivery'
def check_late_delivery(merchant_id):
    return check_delivery_forecast(merchant_id)


# 'check delivery address'
def check_delivery_address(merchant_id):
    # assumption: although the subject is 'check delivery address', the chat message
    # is asking for the delivery forecast. I'm assuming that the AI is classifying
    # messages asking for delivery forecast as 'check delivery address'
    return check_delivery_forecast(merchant_id)


# 'delivery forecast'
def check_delivery_forecast(merchant_id):
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
    return generate_delivery_forecast_msg(track_info)



__load_module__()
# conversation = get_conversation_info('754893')
# print(conversation)
# solve(conversation)
# print(check_connection('530364'))
# print(check_delivery_forecast('849583'))
# print(check_late_delivery('384923'))
# print(check_delivery_address('395023'))

