from db.connection import conn_pool
from flask import request
from psycopg2.extras import RealDictCursor


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_filters(self):
        filters = {
            'role': request.args.get('filter[role]'),
            'city': request.args.get('filter[city]'),
            'event_ids': request.args.get('filter[eventIds]'),
            'case_ids': request.args.get('filter[caseIds]')
        }

        return filters

    def get_users(
        self,
        role=None,
        city=None,
        event_ids=None,
        case_ids=None,
        userId=None
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
                    %(userId)s
                );''',
                {
                    'role': role,
                    'city': city,
                    'event_ids': event_ids,
                    'case_ids': case_ids,
                    'userId': userId
                }
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


# Initializing the users_dao object and preload the prepare statements
users_dao = UsersDao()
