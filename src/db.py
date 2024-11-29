import os
import psycopg2
from dotenv import load_dotenv


def get_connection():
    load_dotenv(os.path.join("..", os.path.dirname(__file__), ".env"))

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    return psycopg2.connect(database="transactions",
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)


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

        result = transactions
        cursor.close
        con.close()
        return result

    except:
        cursor.close
        con.close()

def transaction_window(trans_num_to_find='', trans_unix_time = ''):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT t.trans_amt, m.merch_lat, m.merch_long, t.trans_unix_time, t.trans_is_fraud 
            FROM transaction t
            JOIN  merchant m ON t.merchant_id = m.merchant_id
            WHERE cc_num = (select cc_num from transaction where trans_num = %s) and trans_unix_time <= %s
            ORDER BY trans_unix_time DESC
            LIMIT 13
        """

        cursor.execute(query, (trans_num_to_find, trans_unix_time))

        transactions = cursor.fetchall()

        return transactions

    finally:
        cursor.close()
        conn.close()
