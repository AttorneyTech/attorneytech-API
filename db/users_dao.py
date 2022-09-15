from db.connection import conn_pool
from flask import request
from psycopg2.extras import RealDictCursor


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_filters(self):
        filters = {
            'role': request.args.get('filter[role]', type=str),
            'city': request.args.get('filter[city]', type=str),
            'event_ids': request.args.getlist(
                'filter[eventIds][oneOf]', type=int
            ),
            'case_ids': request.args.getlist(
                'filter[caseIds][oneOf]', type=int
            )
        }
        return filters

    def get_users(
        self,
        role=None,
        city=None,
        event_ids=None,
        case_ids=None,
        user_id=None
    ):
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
                    %(case_ids)s,
                    %(user_id)s
                );''',
                {
                    'role': role,
                    'city': city,
                    'event_ids': event_ids,
                    'case_ids': case_ids,
                    'user_id': user_id
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


# Initializing the users_dao object and preload the prepare statements
users_dao = UsersDao()
