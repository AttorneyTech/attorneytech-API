import psycopg2
from psycopg2 import pool

from common.config import config


class DbConnection:
    '''
    Construct the connection of database
    '''
    def __init__(self):
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.db_name = config.db_name
        self.db_username = config.db_username
        self.db_password = config.db_password

    def create_conn_pool(self):
        try:
            conn_pool = pool.ThreadedConnectionPool(
                minconn=5,
                maxconn=20,
                user=self.db_username,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )

            return conn_pool
        except Exception as err:

            raise err

    # Get the connection to postgreSQL
    # If failed, raise the error
    def get_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_username,
                password=self.db_password
            )

            return conn

        except Exception as err:

            raise err
