import sqlite3
DATABASE = 'simulation-db.db'
TABLE_SALES = 'sales'
TABLE_TRANSACTIONS = 'transactions'
TABLE_RECEIPT = 'receipts'
connection = sqlite3.connect(DATABASE)


def __get(merchant_id, table):
    query_str = f"SELECT * FROM {table} WHERE merchant_id='{merchant_id}';"
    cur = connection.cursor()
    cur.execute(query_str)
    rows = cur.fetchall()
    return rows


def get_sales(merchant_id):
    return __get(merchant_id, TABLE_SALES)


def get_transactions(merchant_id=None):
    return __get(merchant_id, TABLE_TRANSACTIONS)


def get_receipts(merchant_id):
    return __get(merchant_id, TABLE_RECEIPT)


#get_sales('saleid', 'merchant_id')
#get_transactions('transação', 'mercante')
print(get_sales(merchant_id='384923'))