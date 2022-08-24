from flask import make_response
from flask_restful import Resource


from common.error_handler import (
    NotFound,
    InternalServerError
)
from common.logger import logger
from db.users_dao import UsersDao
from serializers.user_serializer import UserSerializer


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user data by user ID
        '''
        user_dao = UsersDao()
        try:
            user_raw_data = user_dao.get_user_by_id(userId)
            if user_raw_data:
                user_response_json_api = UserSerializer.serialize_user_data(
                    user_raw_data,
                    userId
                )
                logger.info('Successful response')

                return make_response(user_response_json_api, 200)
            else:
                error = NotFound(userId)
                logger.error('Resource not found')

                return make_response(error.error_response(), 404)
        except Exception as err:
            error = InternalServerError(
                str(err).replace('\"', '').replace('\n', '')
            )
            logger.error(err)
            return make_response(error.error_response(), 500)
