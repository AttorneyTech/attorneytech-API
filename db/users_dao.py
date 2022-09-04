from db.connection import conn_pool
from db.sql_query import prepare_user_query
from psycopg2.extras import RealDictCursor


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None
    def prepare_query(self):
        try:
            self.conn = conn_pool.getconn(key='users')
            self.cur = self.conn.cursor()
            self.cur.execute(prepare_user_query())
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn, key='users')

    def get_user_by_id(self, userId):
        try:
            self.conn = conn_pool.getconn(key='users')
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(f'EXECUTE get_user_by_id({userId});')
            raw_user = self.cur.fetchall()
            return raw_user
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn, key='users')


# Initializing the users_dao object and preload the prepare statements
users_dao = UsersDao()
users_dao.prepare_query()
