from string import Template

TEMPLATE_RECEIPT_SUCCESSFULL = """Hello, $name, thank you for the message.
According to our records, on $date a transfer of $amount was successfully made to your bank account.
If this is the transfer you're concerned about, we ask to check you bank account again.
"""

TEMPLATE_RECEIPT_UNSUCCESSFULL = """Hello, $name, thank you for the message.
According to our records, we unsuccessfully tried to transfer $amount to your bank account on $date because "$reason".
We apologize for the inconvenience.
We will try to make this transfer again soon.
"""

TEMPLATE_CONNECTION_OK = """Hello, user.
We've checked that all your chips are connected.
We respectfully ask you to check again.
"""

TEMPLATE_CONNECTION_PROBLEM = """Hello, user.
We've checked that the chip(s) with the following id(s): $ids is(are) indeed having connection problems.
$other_messages
Our analysts are working to solve the issue and if necessary your InifnitePay machine will be replaced.
"""
TEMPLATE_CONNECTION_INACTIVE = "Chip $chip_id is inactive. Reason: $reason."
TEMPLATE_CONNECTION_WITHOUT_CONN = "Chip $chip_id is disconnected. We respectfully ask you to check " \
                                   "your Internet connection again."
TEMPLATE_UNDEFINED = """Hello $name, thank you for your message.
We are working in order to solve this problem right now.
If necessary, one of our analysts will contact you.
"""
TEMPLATE_DELIVERY_FORECAST = """Hello, user, thank you for your message!
Your InfinitePay's machine is currently '$status' and the expected delivery date is $date.
"""

TEMPLATE_DELIVERY_ADDRESS = """
The delivery address is St. $street, $neighborhood, $city, $state, $cep.
"""


def generate_receipt_msg(receipt):
    receipt = receipt.values()
    name, date, status, reason, amount = receipt
    if status != 'OK':
        return Template(TEMPLATE_RECEIPT_UNSUCCESSFULL).substitute(name=name, amount=amount, date=date, reason=reason)
    else:
        return Template(TEMPLATE_RECEIPT_SUCCESSFULL).substitute(name=name, date=date, amount=amount)


def generate_connection_msg(chips_status):
    inactive = []
    without_conn = []

    for chip_status in chips_status:
        if chip_status['status'] == 'inactive':
            inactive.append(chip_status)
        elif chip_status['status'] == 'without connection':
            without_conn.append(chip_status)

    msg = None

    msg_queue = []
    if inactive or without_conn:
        ids = [i['id'] for i in inactive] + [w['id'] for w in without_conn]
        for chip in inactive:
            inactive_msg = Template(TEMPLATE_CONNECTION_INACTIVE).substitute(chip_id=chip['id'],
                                                                             reason=chip['description'])
            msg_queue.append(inactive_msg)
        for chip in without_conn:
            without_conn_msg = Template(TEMPLATE_CONNECTION_WITHOUT_CONN).substitute(chip['id'])
        msg_queue = "\n".join(msg_queue)
        msg = Template(TEMPLATE_CONNECTION_PROBLEM).substitute(ids=ids, other_messages=msg_queue)
    else:
        msg = TEMPLATE_CONNECTION_OK
    return msg


def generate_delivery_data_msg():
    pass


def generate_delivery_address_msg():
    pass


def generate_delivery_forecast_msg(track_info):
    status = track_info['status']
    delivery_forecast = track_info['delivery_forecast']
    #neighborhood = address_info['neighborhood']
    #zip_code = address_info['ZIP_code']
    #city = address_info['city']
    #street = address_info['street']
    #state = address_info['state']
    msg = Template(TEMPLATE_DELIVERY_FORECAST).substitute(status=status, date=delivery_forecast)
    return msg

# print(generate_receipt_msg('juliano', 1000, 'data'))
# print(generate_receipt_msg('juliano', 1000, 'data', 'api indisponível'))
