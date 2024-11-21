import psycopg2
import os

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port,
    )