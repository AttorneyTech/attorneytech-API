from db.connection import DbConnection
from db.sql_query import user_query


connection = DbConnection()


class UserDao:
    def __init__(self, userId):
        self.userId = userId

    # Get the raw user data by user id from database
    # If the connection failed, return the error message

    def get_user_by_id(self):
        conn = connection.get_connection()
        try:
            cur = conn.cursor()
        except Exception:
            err = conn

            return err

        # If the get the raw user data failed
        # return the message of syntax error at SQL query

        try:
            cur.execute(user_query(self.userId))
        except Exception:
            err = 'Syntax error at SQL query'

            return err

        # If get the raw user data successfully
        # return the user_raw_data

        else:
            user_raw_data = cur.fetchall()

            return user_raw_data
        finally:
            cur.close()
            conn.close()
