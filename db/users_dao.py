from flask import request
from psycopg2.extras import RealDictCursor

from db.connection import conn_pool


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.filters = request.args
        # self.post_data = request.get_json()

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

    def post_user(self):
        pass
