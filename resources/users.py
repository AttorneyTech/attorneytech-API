from flask import make_response
from flask_restful import Resource

from common.auth import auth
from common.error_handler import BadRequest, InternalServerError
from common.logger import logger
from common.string_handler import string_handler
from db.filter_checker import valid_filters
from db.users_dao import UsersDao
from serializers.users_serializer import UsersSerializer


class Users(Resource):
    @auth.login_required
    def get(self):
        '''Get the list of users'''

        try:
            dao = UsersDao()
            # Check if the filter is valid.
            valid_filters(dao.filters, 'users')
            raw_users = dao.get_users(
                role=dao.filters.get('filter[role]', type=str),
                city=dao.filters.get('filter[city]', type=str),
                event_ids=dao.filters.getlist(
                    'filter[eventIds][oneOf]', type=int
                ),
                case_ids=dao.filters.getlist(
                    'filter[caseIds][oneOf]', type=int
                )
            )
            users_objects = UsersSerializer.raw_users_serializer(raw_users)
            users_response = UsersSerializer.users_response(users_objects)
            return make_response(users_response, 200)
        except ValueError as err:
            err_message = string_handler(err)
            error = BadRequest(err_message)
            logger.error(err_message)
            return make_response(error.error_response(), 400)
        except Exception as err:
            err_message = string_handler(err)
            error = InternalServerError(err_message)
            logger.error(err_message)
            return make_response(error.error_response(), 500)
