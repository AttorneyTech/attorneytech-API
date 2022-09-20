from flask import make_response
from flask_restful import Resource

from common.auth import auth
from common.error_handler import (
    NotFound,
    InternalServerError
)
from common.logger import logger
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
                user_response = UsersSerializer.user_response(user_object)
                return make_response(user_response, 200)
            else:
                detail = (
                    f'The resource requested (user ID:{user_id}) not found.'
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
