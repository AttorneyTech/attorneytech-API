from flask import make_response
from flask_restful import Resource


from common.auth import auth
from common.error_handler import (
    NotFound,
    InternalServerError
)
from common.logger import logger
from db.users_dao import users_dao
from serializers.user_serializer import UserSerializer


class User(Resource):
    @auth.login_required
    def get(self, userId):
        '''
        Get the specific user data by user ID
        '''
        try:
            raw_user = users_dao.get_user_by_id(userId)
            if raw_user:
                user_response_json = UserSerializer.serialize_raw_user(
                    raw_user
                )
                return make_response(user_response_json, 200)
            else:
                detail = (
                    f'The resource requested (user ID:{userId}) was not found.'
                )
                error = NotFound(detail)
                logger.error(detail)
                return make_response(error.error_response(), 404)
        except Exception as err:
            error = InternalServerError(
                str(err).replace('\"', '').replace('\n', '')
            )
            logger.error(err)
            return make_response(error.error_response(), 500)
