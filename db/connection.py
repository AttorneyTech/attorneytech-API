import psycopg2
from common.config import read_config_of_db


config = read_config_of_db()

db_host = config['db_host']
db_port = config['port']
db_name = config['db_name']
db_username = config['db_username']
db_password = config['db_password']


# Construct the connection to database
def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_username,
        password=db_password
    )
    return conn
