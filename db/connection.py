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
        self.db_poolmin = config.db_poolmin
        self.db_poolmax = config.db_poolmax

    def create_conn_pool(self):
        try:
            conn_pool = pool.ThreadedConnectionPool(
                minconn=self.db_poolmin,
                maxconn=self.db_poolmax,
                user=self.db_username,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )
            return conn_pool
        except Exception as err:
            raise err


connection = DbConnection()
conn_pool = connection.create_conn_pool()
