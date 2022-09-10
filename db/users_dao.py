from db.connection import conn_pool
from psycopg2.extras import RealDictCursor


class UsersDao:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_users(
        self,
        role='NULL',
        city='NULL',
        events_id='NULL',
        cases_id='NULL',
        userId='NULL'
    ):
        '''
        Connect to PostgreSQL and get the raw data
        of a specific user by user ID
        '''
        try:
            self.conn = conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(
                f'''
                EXECUTE get_users(
                    {role},
                    {city},
                    {events_id},
                    {cases_id},
                    {userId}
                );
                '''
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
