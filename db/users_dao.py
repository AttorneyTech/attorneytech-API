from flask import request
from psycopg2.extras import RealDictCursor

from db.connection import conn_pool


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

    def get_user_email(self, email):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE get_user_email(%(email)s);',
                {'email': email}
            )
            raw_user = self.cur.fetchone()
            return raw_user
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def get_user_username(self, username):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE get_user_username(%(username)s);',
                {'username': username}
            )
            raw_user = self.cur.fetchone()
            return raw_user
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def get_case_ids(self, case_ids):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE get_case_ids(%(case_ids)s);',
                {'case_ids': case_ids}
            )
            raw_user = self.cur.fetchall()
            return raw_user
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def get_event_ids_by_case_ids(self, case_ids):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE get_event_ids_by_case_ids(%(case_ids)s);',
                {'case_ids': case_ids}
            )
            raw_user = self.cur.fetchone()
            return raw_user
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def post_user(self, valid_data):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor()
            attributes = valid_data['data']['attributes']
            address = valid_data['data']['attributes']['address']
            self.cur.execute(
                '''EXECUTE post_user(
                    %(role)s,
                    %(username)s,
                    %(password)s,
                    %(first_name)s,
                    %(middle_name)s,
                    %(last_name)s,
                    %(email)s,
                    %(phone)s,
                    %(street_name)s,
                    %(district)s,
                    %(city)s,
                    %(zip_code)s
                );
                ''',
                {
                    'role': attributes.get('role'),
                    'username': attributes.get('username'),
                    'password': attributes.get('password'),
                    'first_name': attributes.get('firstName'),
                    'middle_name': attributes.get('middleName'),
                    'last_name': attributes.get('lastName'),
                    'email': attributes.get('email'),
                    'phone': attributes.get('phone'),
                    'street_name': address.get('addressLine1'),
                    'district': address.get('addressLine2'),
                    'city': address.get('city'),
                    'zip_code': address.get('zipCode')
                }
            )
            self.conn.commit()
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)
