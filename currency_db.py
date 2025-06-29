import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def upsert_currency_data(currency: str, rate: float):
    table = os.getenv('CURRENCY_TABLE_NAME', 'currency_currencydata')
    query = f"""
    INSERT INTO {table} (currency, rate)
    VALUES (%s, %s)
    ON CONFLICT (currency) DO UPDATE
    SET rate = EXCLUDED.rate;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (currency, rate))

def get_all_currency_data():
    table = os.getenv('CURRENCY_TABLE_NAME', 'currency_currencydata')
    query = f"SELECT currency, rate FROM {table}"
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return [{"currency": row[0], "rate": row[1]} for row in cursor.fetchall()]