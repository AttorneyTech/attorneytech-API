from common.logger import Logger
from db.connection import DbConnection
from db.sql_query import user_query


api_logger = Logger().create_logger()
connection = DbConnection()


class UserDao:
    def __init__(self, userId):
        self.userId = userId

    def get_data_from_db(self):
        conn = connection.connection()
        cur = conn.cursor()
        cur.execute(user_query(self.userId))
        response = cur.fetchall()

        cur.close()
        conn.close()

        return response
