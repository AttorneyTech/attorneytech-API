from flask import make_response
from flask_restful import Resource

from common.auth import auth
from common.error_handler import (
    bad_request,
    error_handler,
    internal_server_error
)
from common.string_handler import error_detail_handler
from common.filter_handler import enums_check, filters_to_list
from common.logger import logger
from db.users_dao import UsersDao
from serializers.users_serializer import UsersSerializer


class Users(Resource):
    @auth.login_required
    def get(self):
        '''Get the list of users'''

        try:
            dao = UsersDao()
            # Check if the filter is valid.
            enums_check(dao.filters, 'users')
            raw_event_ids = dao.filters.get('filter[eventIds][oneOf]')
            raw_case_ids = dao.filters.get('filter[caseIds][oneOf]')
            raw_users = dao.get_users(
                role=dao.filters.get('filter[role]'),
                city=dao.filters.get('filter[city]'),
                event_ids=filters_to_list(
                    raw_event_ids, data_type=int, default_value=-1
                ),
                case_ids=filters_to_list(
                    raw_case_ids, data_type=int, default_value=-1
                )
            )
            users_objects = UsersSerializer.raw_users_serializer(raw_users)
            serialized_users = UsersSerializer.users_response(users_objects)
            return make_response(serialized_users, 200)
        except ValueError as err:
            # Unpack the args to get the list of details
            details = err.args[0]
            details = [error_detail_handler(detail) for detail in details]
            logger.error(details)
            error_objects = bad_request(details)
            error_response = error_handler(error_objects)
            return make_response(error_response, 400)
        except Exception as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_object = internal_server_error(detail)
            error_response = error_handler(error_object)
            return make_response(error_response, 500)

    @auth.login_required
    def post(self):
        '''Create a user'''
        pass
