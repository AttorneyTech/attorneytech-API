from flask import request
from psycopg2.extras import RealDictCursor

from common.string_handler import users_attributes
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

    def get_email_username(self, email, username):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                'EXECUTE validate_email_username(%(email)s, %(username)s);',
                {'email': email, 'username': username}
            )
            raw_result = self.cur.fetchall()
            return raw_result
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
            raw_user_id = self.cur.fetchone()
            return raw_user_id
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def post_cases_users(self, case_ids, user_id):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor()
            if case_ids:
                self.cur.execute(
                    'EXECUTE post_cases_users(%(case_ids)s, %(user_id)s);',
                    {'case_ids': case_ids, 'user_id': user_id}
                )
            else:
                self.cur.execute(
                    '''
                    EXECUTE post_empty_cases_users(%(case_ids)s, %(user_id)s);
                    ''',
                    {'case_ids': case_ids, 'user_id': user_id}
                )
            self.conn.commit()
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def patch_user(self, valid_data, user_id):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor()
            attributes = valid_data.get('data').get('attributes')

            set_clauses = []
            values = []
            for attr, value in attributes.items():
                if attr in users_attributes:
                    attr = users_attributes[attr]
                if attr in ['caseIds', 'eventIds']:
                    continue
                set_clauses.append(f'{attr} = %s')
                values.append(value)

            if not set_clauses:
                return

            set_clause = ', '.join(set_clauses)
            sql = f'UPDATE users SET {set_clause} WHERE id = %s'
            values.append(user_id)

            self.cur.execute(sql, tuple(values))
            self.conn.commit()
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def patch_cases_users(self, case_ids, user_id):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor()
            self.cur.execute(
                'EXECUTE del_exist_cases_users(%(user_id)s);',
                {'user_id': user_id}
            )
            self.cur.execute(
                'EXECUTE post_cases_users(%(case_ids)s, %(user_id)s);',
                {'case_ids': case_ids, 'user_id': user_id}
            )
            self.conn.commit()
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)
