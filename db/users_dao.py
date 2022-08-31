from db.connection import conn_pool
from db.sql_query import prepare_user_query


class UsersDao:
    def prepare_query(self):
        conn, cur = None, None
        try:
            conn = conn_pool.getconn()
            cur = conn.cursor()
            cur.execute(prepare_user_query())
        except Exception as err:

            raise err
        finally:
            if cur and conn:
                cur.close()
                conn_pool.putconn(conn=conn)

    def get_user_by_id(self, userId):
        conn, cur = None, None
        try:
            conn = conn_pool.getconn()
            cur = conn.cursor()
            cur.execute(f'EXECUTE get_user_by_id({userId});')
            user_raw_data = cur.fetchall()

            return user_raw_data
        except Exception as err:

            raise err
        finally:
            if cur and conn:
                cur.close()
                conn_pool.putconn(conn=conn)


users_dao = UsersDao()
users_dao.prepare_query()
