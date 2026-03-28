import psycopg2
from config import conf1g
def get_connection():
    return psycopg2.connect(**conf1g)
def close_connection(conn):
    if conn:
        conn.close()
