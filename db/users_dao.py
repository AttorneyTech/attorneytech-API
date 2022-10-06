from db.connection import conn_pool
from flask import request
from psycopg2.extras import RealDictCursor


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.filters = request.args

    def get_user_by_id(self, user_id):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE get_user_by_id(%(user_id)s);', {'user_id': user_id}
            )
            raw_users = self.cur.fetchall()
            return raw_users
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def get_users(self, role, city, event_ids, case_ids):
        '''
        Connect to PostgreSQL and get the raw data
        of a specific user by user ID
        '''

        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                '''EXECUTE get_users(
                    %(role)s,
                    %(city)s,
                    %(event_ids)s,
                    %(case_ids)s
                );''',
                {
                    'role': role,
                    'city': city,
                    'event_ids': event_ids,
                    'case_ids': case_ids
                }
            )
            raw_users = self.cur.fetchall()
            return raw_users
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)
