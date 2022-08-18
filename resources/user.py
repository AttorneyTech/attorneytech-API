from flask import make_response
from flask_restful import Resource

from common.logger import Logger
from common.error_handler import NotFound, InternalServerError
from db.connection import DbConnection
from db.user_dao import UserDao
from models.user_model import UserModel


api_logger = Logger().create_logger()
connection = DbConnection()


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user by user ID
        '''
        # Access data by UserDao
        user_dao = UserDao(userId)

        try:
            response = user_dao.get_data_from_db()

        except Exception as e:
            error_message_raw = str(e).split()
            error_message = ' '.join(
                    error_message_raw[:3] +
                    error_message_raw[8:9] +
                    error_message_raw[10:13]
                )
            error = InternalServerError(error_message)
            api_logger.error(error_message)

            return make_response(error.error_response(), 500)

        else:
            if response:
                response = UserModel.get_user_by_id(response, userId)
                api_logger.info('Successful response')

                return make_response(response, 200)
            else:
                error = NotFound()
                api_logger.error('Resource not found')

                return make_response(error.error_response(), 404)
