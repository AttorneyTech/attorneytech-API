from flask import make_response
from flask_restful import Resource

from common.auth import auth
from common.error_handler import InternalServerError
from common.logger import logger
from db.users_dao import UsersDao
from serializers.users_serializer import UsersSerializer


class Users(Resource):
    @auth.login_required
    def get(self):
        '''Get the list of users'''

        try:
            users_dao = UsersDao()
            raw_users = users_dao.get_users(
                role=users_dao.filters.get('filter[role]', type=str),
                city=users_dao.filters.get('filter[city]', type=str),
                event_ids=users_dao.filters.getlist(
                    'filter[eventIds][oneOf]', type=int
                ),
                case_ids=users_dao.filters.getlist(
                    'filter[caseIds][oneOf]', type=int
                )
            )
            users_objects = UsersSerializer.raw_users_serializer(raw_users)
            user_response = UsersSerializer.users_response(users_objects)
            return make_response(user_response, 200)
        except Exception as err:
            error = InternalServerError(
                str(err).replace('\"', '').replace('\n', '')
            )
            logger.error(err)
            return make_response(error.error_response(), 500)
