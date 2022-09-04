import atexit
import sys
import traceback

from psycopg2 import pool

from common.config import config
from common.logger import logger
from db.sql_query import prepare_sql_query


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
    def __init__(self):
        self.conn = None
        self.cur = None

    def create_pool(self):
        '''
        Create a pool of connection to PostgreSQL
        '''
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

    def db_validate_and_prepare(self):
        '''
        Validate database connection. If validated,
        run the PREPARE statements or raise an error
        '''
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor()
            self.cur.execute('SELECT 1;')
            self.cur.execute(prepare_sql_query())
        except Exception as err:
            logger.error(err)
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)


@atexit.register
def close_pool():
    '''
    Close the pool when application is stopped
    '''
    conn_pool.closeall()


db_connection = DbConnection()
conn_pool = db_connection.create_pool()
db_connection.db_validate_and_prepare()
