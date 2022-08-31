# from db.connection import DbConnection
from db.connection import conn_pool
from db.sql_query import user_query


class UsersDao:
    def __init__(self):
        self.conn_pool = conn_pool

    # Connect to database and create the cursor
    # to execute SQL query
    # If failed in the progress above,
    # raise the error
    def get_user_by_id(self, userId):
        conn, cur = None, None
        try:
            conn = self.conn_pool.getconn()
            cur = conn.cursor()
            cur.execute(user_query(userId))
            user_raw_data = cur.fetchall()

            return user_raw_data
        except Exception as err:

            raise err
        finally:
            if cur and conn:
                cur.close()
                self.conn_pool.putconn(conn=conn)
