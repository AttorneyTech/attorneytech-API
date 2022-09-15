import atexit

from psycopg2 import pool

from common.config import config_db
from common.logger import logger
from db.sql_query import prepare_statements


class DbConnection:
    def __init__(self):
        self.conn = None
        self.cur = None

    def create_pool(self):
        '''Create a pool of connection to PostgreSQL'''

        try:
            conn_pool = pool.ThreadedConnectionPool(
                minconn=config_db['poolmin'],
                maxconn=config_db['poolmax'],
                user=config_db['username'],
                password=config_db['password'],
                host=config_db['host'],
                port=config_db['port'],
                database=config_db['db_name']
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
            for statement in prepare_statements:
                self.cur.execute(statement)
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
    '''Close the pool when application is stopped'''

    conn_pool.closeall()


db_connection = DbConnection()
conn_pool = db_connection.create_pool()
db_connection.db_validate_and_prepare()
