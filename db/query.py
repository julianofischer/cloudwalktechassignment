import os.path
import sqlite3
from pathlib import Path

BASE_DIR = str(Path(__file__).parent.parent)
DATABASE = os.path.join(BASE_DIR, 'simulation-db.db')
TABLE_SALES = 'sales'
TABLE_TRANSACTIONS = 'transactions'
TABLE_RECEIPT = 'receipt'
connection = sqlite3.connect(DATABASE)


def _get(merchant_id, table):
    """ Helper method which construct database queries based on merchant id and table name.
    :param merchant_id: the merchant unique id
    :param table: the table name
    :return: a list containing rows returned by the query as tuples
    """
    query_str = f"SELECT * FROM {table} WHERE merchant_id='{merchant_id}'"
    cur = connection.cursor()
    cur.execute(query_str)
    rows = cur.fetchall()
    return rows


def get_sales(merchant_id: str):
    """ Given a merchant id, returns a list of sales linked to him.
    :param merchant_id: the merchant unique id
    :return: a list of tuples containing information regarding sales linked to the merchant
    (34854, 558392, 'CHIP37652', '2021-02-01 12:00:00-03:00', 'done', 'delivered')
    (id_sale, merchant_id, chip_id, created_at, status, description)
    """
    return _get(merchant_id, TABLE_SALES)


def get_transactions(merchant_id=None):
    """ Given a merchant id, returns a list of transactions linked to him.
    :param merchant_id: the merchant unique id
    :return: a list of tuples containing information regarding transactions linked to the merchant
    (374290, 558392, '2021-12-21 13:00:00-03:00', 127.4)
    (transaction_id, merchant_id, created_at, value)
    """
    return _get(merchant_id, TABLE_TRANSACTIONS)


def get_receipts(merchant_id: str) -> list:
    """ Given a merchant id, returns a list of receipts linked to him.
        :param merchant_id: the merchant unique id
        :return: a list of dicts containing information regarding transactions linked to the merchant
        dict format: {'merchant_id': 558392, 'created_at': '2021-12-22 01:00:00-03:00', 'status': 'failed',
        'description': "bank's API is unavailable", 'value': 177.4}
        """
    receipts = _get(merchant_id, TABLE_RECEIPT)
    ret = []
    for receipt in receipts:
        d = {}
        d['merchant_id'], d['created_at'], d['status'], d['description'], d['value'] = receipt
        ret.append(d)
    return ret

# print(get_sales('558392'))
# print(get_transactions('558392'))
#print(get_receipts('558392'))