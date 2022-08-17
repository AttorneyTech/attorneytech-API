import psycopg2
from common.config import read_config


config = read_config()
db_host = config['database']['db_host']
db_port = config['database']['port']
db_name = config['database']['db_name']
db_username = config['database']['db_username']
db_password = config['database']['db_password']


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
