from werkzeug.security import generate_password_hash

from db.connection import DbConnection
from db.sql_query import user_verify_query


connection = DbConnection()


class UserVerifyDao:
    def __init__(self, username):
        self.username = username

    # Get the user raw data from database
    # If the connection failed, return the error message

    def verify_user_from_db(self):
        conn = connection.get_connection()
        try:
            cur = conn.cursor()
        except Exception:
            err = conn

            return err

        # If the get the raw user data failed
        # return the message of syntax error at SQL query

        try:
            cur.execute(user_verify_query(self.username))
        except Exception as err:
            err = 'Syntax error at SQL query'

            return err

        # If get the raw user data successfully
        # return the user_login_data

        else:
            user_login_raw_data = cur.fetchall()
            if user_login_raw_data:
                login_username = user_login_raw_data[0][0]
                login_password = generate_password_hash(
                        user_login_raw_data[0][1]
                    )
                user_login_data = {login_username: login_password}

                return user_login_data

        finally:
            cur.close()
            conn.close()
