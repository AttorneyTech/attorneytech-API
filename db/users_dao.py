from typing import List, Tuple

from flask import request
from psycopg2.extras import RealDictCursor

from common.dict_handler import get_patch_user_values
from db.connection import conn_pool


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.filters = request.args

    def execute_query(
            self,
            queries: List[Tuple],
            commit: bool = False,
            fetch_type: str = None
    ):
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

            for query, param in queries:
                self.cur.execute(query, param)

            fetch_methods = {
                'all': self.cur.fetchall,
                'one': self.cur.fetchone
            }

            if commit:
                self.conn.commit()
            if fetch_type in fetch_methods:
                result = fetch_methods[fetch_type]()
                return result
        except Exception as err:
            raise err
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                conn_pool.putconn(conn=self.conn)

    def get_user_by_id(self, user_id):
        query_param_pairs = [
            ('EXECUTE get_user_by_id(%(user_id)s);', {'user_id': user_id})
        ]

        return self.execute_query(query_param_pairs, fetch_type='all')

    def get_users(self, role, city, event_ids, case_ids):
        query_param_pairs = [
            (
                '''
                EXECUTE get_users(
                    %(role)s, %(city)s, %(event_ids)s, %(case_ids)s
                );
                ''',
                {
                    'role': role,
                    'city': city,
                    'event_ids': event_ids,
                    'case_ids': case_ids
                }
            )
        ]
        return self.execute_query(query_param_pairs, fetch_type='all')

    def get_email_username(self, email, username):
        query_param_pairs = [
            (
                'EXECUTE validate_email_username(%(email)s, %(username)s);',
                {'email': email, 'username': username}
            )
        ]
        return self.execute_query(query_param_pairs, fetch_type='all')

    def get_case_ids(self, case_ids):
        query_param_pairs = [
            (
                'EXECUTE get_case_ids(%(case_ids)s);',
                {'case_ids': case_ids}
            )
        ]
        return self.execute_query(query_param_pairs, fetch_type='all')

    def get_event_ids_by_case_ids(self, case_ids):
        query_param_pairs = [
            (
                'EXECUTE get_event_ids_by_case_ids(%(case_ids)s);',
                {'case_ids': case_ids}
            )
        ]
        return self.execute_query(query_param_pairs, fetch_type='one')

    def post_user(self, valid_data):
        attributes = valid_data['data']['attributes']
        address = valid_data['data']['attributes']['address']
        query_param_pairs = [
            (
                '''
                EXECUTE post_user(
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
        ]
        return self.execute_query(
            query_param_pairs, commit=True, fetch_type='one'
        )

    def post_cases_users(self, case_ids, user_id):
        if case_ids:
            query = 'EXECUTE post_cases_users(%(case_ids)s, %(user_id)s);'
        else:
            query = '''
                EXECUTE post_empty_cases_users(%(case_ids)s, %(user_id)s);
            '''

        param = {'case_ids': case_ids, 'user_id': user_id}
        query_param_pairs = [(query, param)]

        return self.execute_query(query_param_pairs, commit=True)

    def post_empty_cases_users(self, case_ids, user_id):
        query_param_pairs = [
            (
                'EXECUTE post_empty_cases_users(%(case_ids)s, %(user_id)s);',
                {'case_ids': case_ids, 'user_id': user_id}
            )
        ]

        return self.execute_query(query_param_pairs, commit=True)

    def patch_user(self, valid_data, user_id):
        '''
        Since there is a need for dynamic sql query,
        prepare is not used here.
        Suppose now patch first Name and middle Name.

        :set_clauses: ['middle_name = %s', 'first_name = %s']
        :set_clause: first_name = %s, middle_name = %s
        :values: ['new_middle_name', 'new_first_name', 'user_id']

        Then wrap values in tuple and map to set_clause string.
        '''

        patch_attributes = valid_data.get('data').get('attributes')
        set_columns, patch_values = get_patch_user_values(patch_attributes)

        if not set_columns:
            return

        set_column = ', '.join(set_columns)
        patch_values.append(user_id)
        query_param_pairs = [
            (
                f'UPDATE users SET {set_column} WHERE id = %s',
                tuple(patch_values)
            )
        ]
        return self.execute_query(query_param_pairs, commit=True)

    def patch_cases_users(self, case_ids, user_id):
        del_query = 'EXECUTE del_cases_users(%(user_id)s);'
        post_query = 'EXECUTE post_cases_users(%(case_ids)s, %(user_id)s);'
        empty_post_query = '''
            EXECUTE post_empty_cases_users(%(case_ids)s, %(user_id)s);
        '''
        queries = [del_query]
        params = [{'user_id': user_id}]

        if case_ids:
            queries.append(post_query)
        else:
            queries.append(empty_post_query)

        params.append({'case_ids': case_ids, 'user_id': user_id})
        query_param_pairs = list(zip(queries, params))

        return self.execute_query(query_param_pairs, commit=True)
