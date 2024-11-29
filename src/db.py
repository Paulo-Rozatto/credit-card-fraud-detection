import os
import psycopg2
from dotenv import load_dotenv


def get_connection():
    # load_dotenv(os.path.join("..", os.path.dirname(__file__), ".env"))
    load_dotenv("/home/paulo/Projects/credit-card-fraud-detection/.env")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    return psycopg2.connect(database="transactions",
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)

#  select trans_num, trans_unix_time from transaction order by trans_unix_time desc limit 10


def get_transactions_num(limit=10):
    try:
        con = get_connection()
        cursor = con.cursor()
        query = """
            SELECT trans_num, trans_unix_time 
            FROM transaction 
            ORDER BY trans_unix_time DESC 
            LIMIT %s;
        """

        cursor.execute(query, (limit,))
        transactions = cursor.fetchall()

        # result = {f: v for f, v in zip(field_names, transactions)}
        result = transactions
        cursor.close
        con.close()
        return result

    except:
        cursor.close
        con.close()

def transaction_window(trans_num_to_find='413636e759663f264aae1819a4d4f231', trans_unix_time = ''):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("Start")
        print(trans_num_to_find)

        query = """
            SELECT t.trans_amt, m.merch_lat, m.merch_long, t.trans_unix_time, t.trans_is_fraud 
            FROM transaction t
            JOIN  merchant m ON t.merchant_id = m.merchant_id
            WHERE cc_num = (select cc_num from transaction where trans_num = %s) and trans_unix_time <= %s
            ORDER BY trans_unix_time DESC
            LIMIT 13
        """

        # Query para obter a transação e as 12 anteriores
#         query = """
# WITH OrderedTransactions AS (
#     SELECT
#         t.trans_num,
#         t.trans_amt,
#         m.merch_lat,
#         m.merch_long,
#         t.trans_unix_time,
#         t.trans_is_fraud,
#         ROW_NUMBER() OVER (ORDER BY t.trans_unix_time ASC) AS rn
#     FROM
#         transaction t
#     JOIN
#         merchant m ON t.merchant_id = m.merchant_id
#     WHERE
#         t.trans_unix_time <= (
#             SELECT trans_unix_time
#             FROM transaction
#             WHERE trans_num = %s
#         )
# ),
# TargetTransaction AS (
#     SELECT rn
#     FROM OrderedTransactions
#     WHERE trans_num = %s
# )
# SELECT
#     ot.trans_amt, ot.merch_lat, ot.merch_long, ot.trans_unix_time, ot.trans_is_fraud
# FROM
#     OrderedTransactions ot
# JOIN
#     TargetTransaction tt ON ot.rn BETWEEN tt.rn - 12 AND tt.rn
# ORDER BY
#     ot.rn ASC;
# """

        cursor.execute(query, (trans_num_to_find, trans_unix_time))

        transactions = cursor.fetchall()

        field_names = [
            'amt_0', 'merch_lat_0', 'merch_long_0', 'unix_time_0', 'is_fraud_0',
            'amt_1', 'merch_lat_1', 'merch_long_1', 'unix_time_1', 'is_fraud_1',
            'amt_2', 'merch_lat_2', 'merch_long_2', 'unix_time_2', 'is_fraud_2',
            'amt_3', 'merch_lat_3', 'merch_long_3', 'unix_time_3', 'is_fraud_3',
            'amt_4', 'merch_lat_4', 'merch_long_4', 'unix_time_4', 'is_fraud_4',
            'amt_5', 'merch_lat_5', 'merch_long_5', 'unix_time_5', 'is_fraud_5',
            'amt_6', 'merch_lat_6', 'merch_long_6', 'unix_time_6', 'is_fraud_6',
            'amt_7', 'merch_lat_7', 'merch_long_7', 'unix_time_7', 'is_fraud_7',
            'amt_8', 'merch_lat_8', 'merch_long_8', 'unix_time_8', 'is_fraud_8',
            'amt_9', 'merch_lat_9', 'merch_long_9', 'unix_time_9', 'is_fraud_9',
            'amt_10', 'merch_lat_10', 'merch_long_10', 'unix_time_10',
            'is_fraud_10', 'amt_11', 'merch_lat_11', 'merch_long_11',
            'unix_time_11', 'is_fraud_11', 'amt', 'merch_lat', 'merch_long',
            'unix_time'
        ]

        print(transactions)
        return transactions

    finally:
        cursor.close()
        conn.close()

# transaction_window()


# def get_transactions_num(limit = 10):
#     try:
#         con = get_connection()
#         cursor = con.cursor()
#     except:
#         cursor.close
#         con.close()
