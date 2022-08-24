from db.connection import DbConnection
from db.sql_query import user_query


class UserDao:
    def __init__(self):
        self.connection = DbConnection()

    # Get the raw user data by user id from database
    # If the connection failed, return the error message

    def get_user_by_id(self, userId):
        try:
            conn = self.connection.get_connection()
            cur = conn.cursor()
            cur.execute(user_query(userId))
            user_raw_data = cur.fetchall()
        except Exception as err:

            raise err
        else:
            cur.close()
            conn.close()
            return user_raw_data
