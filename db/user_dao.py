from flask import make_response

from common.logger import Logger
from common.error_handler import InternalServerError
from db.connection import DbConnection
from db.sql_query import user_query


api_logger = Logger().create_logger()
connection = DbConnection()


class UserDao:
    def __init__(self, userId):
        self.userId = userId

    def get_data_from_db(self):
        try:
            conn = connection.connection()
        except Exception as e:
            error_message = str(e)
            error = InternalServerError(error_message)
            api_logger.error(error_message)
            return make_response(error.error_response(), 500)

        cur = conn.cursor()
        cur.execute(user_query(self.userId))
        response = cur.fetchall()

        cur.close()
        conn.close()

        return response
