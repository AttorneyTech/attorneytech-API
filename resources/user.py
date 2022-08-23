from flask import make_response
from flask_restful import Resource


from common.error_handler import (
    NotFound,
    InternalServerError
)
from common.logger import Logger
from db.connection import DbConnection
from db.user_dao import UserDao
from serializers.user_serializer import UserSerializer


api_logger = Logger().create_logger()
connection = DbConnection()


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user data by user ID
        '''
        user_dao = UserDao(userId)
        user_raw_data = user_dao.get_user_by_id()

        # If user_raw_data
        if type(user_raw_data) is str:
            err = user_raw_data
            error = InternalServerError(err)
            api_logger.error(err)

            return make_response(error.error_response(), 500)
        elif user_raw_data:
            user_response_json_api = UserSerializer.serialize_user_data(
                user_raw_data,
                userId
            )
            api_logger.info('Successful response')

            return make_response(user_response_json_api, 200)
        else:
            error = NotFound(userId)
            api_logger.error('Resource not found')

            return make_response(error.error_response(), 404)
