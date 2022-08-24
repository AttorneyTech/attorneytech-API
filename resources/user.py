from flask import make_response
from flask_restful import Resource


from common.error_handler import (
    NotFound,
    InternalServerError
)
from common.logger import Logger
from db.user_dao import UserDao
from serializers.user_serializer import UserSerializer


api_logger = Logger().create_logger()


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user data by user ID
        '''
        user_dao = UserDao()
        try:
            user_raw_data = user_dao.get_user_by_id(userId)
            if user_raw_data:
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
        except Exception as err:
            error = InternalServerError(
                str(err).replace('\"', '').replace('\n', '')
            )
            api_logger.error(err)
            return make_response(error.error_response(), 500)
