import sqlite3
DATABASE = '../simulation-db.db'
TABLE_SALES = 'sales'
TABLE_TRANSACTIONS = 'transactions'
TABLE_RECEIPT = 'receipt'
connection = sqlite3.connect(DATABASE)


def __get(merchant_id, table):
    query_str = f"SELECT * FROM {table} WHERE merchant_id='{merchant_id}'"
    cur = connection.cursor()
    cur.execute(query_str)
    rows = cur.fetchall()
    return rows


def get_sales(merchant_id):
    # print('get_sales: '+merchant_id)
    return __get(merchant_id, TABLE_SALES)


def get_transactions(merchant_id=None):
    return __get(merchant_id, TABLE_TRANSACTIONS)


def get_receipts(merchant_id):
    receipts = __get(merchant_id, TABLE_RECEIPT)
    ret = []
    for receipt in receipts:
        d = {}
        d['merchant_id'], d['created_at'], d['status'], d['description'], d['value'] = receipt
        ret.append(d)
    return ret