from flask import make_response
from flask_restful import Resource

from common.auth import auth
from common.error_handler import (
    internal_server_error,
    not_found
)
from common.logger import logger
from common.string_handler import error_detail_handler
from db.users_dao import UsersDao
from serializers.users_serializer import UsersSerializer


class User(Resource):
    @auth.login_required
    def get(self, user_id):
        '''Get the specific user data by user ID'''

        try:
            dao = UsersDao
            raw_user = dao.get_user_by_id(self, user_id)
            if raw_user:
                user_object = UsersSerializer.raw_user_serializer(raw_user)
                serialized_user = UsersSerializer.user_response(user_object)
                return make_response(serialized_user, 200)
            else:
                detail = (
                    f'The resource requested (user ID:{user_id}) not found.'
                )
                logger.error(detail)
                error_response = not_found(detail)
                return make_response(error_response, 404)
        except Exception as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_response = internal_server_error(detail)
            return make_response(error_response, 500)
