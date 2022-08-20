from werkzeug.security import generate_password_hash

from db.connection import DbConnection
from db.sql_query import user_verify_query


connection = DbConnection()


class UserVerifyDao:
    def __init__(self, username):
        self.username = username

    # Getting raw data from database

    def get_data_from_db(self):
        conn = connection.connection()
        cur = conn.cursor()
        cur.execute(user_verify_query(self.username))
        user_login_raw_data = cur.fetchall()

        cur.close()
        conn.close()

        if user_login_raw_data:
            login_username = user_login_raw_data[0][0]
            login_password = generate_password_hash(user_login_raw_data[0][1])
            user_login_data = {login_username: login_password}

            return user_login_data
