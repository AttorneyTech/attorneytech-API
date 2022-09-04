import atexit
import sys
import traceback

from psycopg2 import pool

from common.config import config


# Get the configurations of database
try:
    config_db = config['database']
    host = config_db['host']
    port = config_db['port']
    db_name = config_db['db_name']
    username = config_db['username']
    password = config_db['password']
    poolmin = config_db['poolmin']
    poolmax = config_db['poolmax']
except Exception:
    traceback.print_exc()
    sys.exit()


class DbConnection:
    '''
    Construct the connection of database
    '''
    def create_conn_pool(self):
        try:
            conn_pool = pool.ThreadedConnectionPool(
                minconn=poolmin,
                maxconn=poolmax,
                user=username,
                password=password,
                host=host,
                port=port,
                database=db_name
            )
            return conn_pool
        except Exception as err:
            raise err


# Close the pool when application is stopped
@atexit.register
def close_pool():
    conn_pool.closeall()


connection = DbConnection()
conn_pool = connection.create_conn_pool()
