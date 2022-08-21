from db.connection import DbConnection
from db.sql_query import user_query


connection = DbConnection()


class UserDao:
    def __init__(self, userId):
        self.userId = userId

    # Getting raw data from database

    def get_data_from_db(self):
        conn = connection.connection()
        try:
            conn = connection.connection()
            cur = conn.cursor()
            cur.execute(user_query(self.userId))

        except Exception as e:
            return e

        else:
            user_raw_data = cur.fetchall()

        finally:
            cur.close()
            conn.close()

        return user_raw_data
