from db.connection import conn_pool
from db.sql_query import user_query


class UsersDao:
    def get_user_by_id(self, userId):
        conn, cur = None, None
        print('***********')
        print('in user_dao.py')
        print(id(conn_pool))
        print('***********')
        try:
            conn = conn_pool.getconn()
            cur = conn.cursor()
            cur.execute(user_query(userId))
            user_raw_data = cur.fetchall()

            return user_raw_data
        except Exception as err:

            raise err
        finally:
            if cur and conn:
                cur.close()
                conn_pool.putconn(conn=conn)
