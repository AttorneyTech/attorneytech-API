import json

from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from common.auth import auth
from common.error_handler import (
    bad_request,
    conflict,
    error_handler,
    internal_server_error
)
from common.filter_handler import enums_check, filters_to_list
from common.logger import logger
from common.string_handler import error_detail_handler
from common.validate_data import validate_post_user
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
        '''
        Create a user.
        If something missed in post data or the format are wrong based on
        schema of users, it will return the details with 400 bad request.
        And if something are conflict with exist users, it will return the
        details with 409 conflict.
        '''

        try:
            unchecked_data = request.get_json()
            validate_post_user(unchecked_data)
        except ValidationError as err:
            details = []
            detail = error_detail_handler(json.dumps(err.messages))
            details.append(detail)
            logger.error(details)
            error_object = bad_request(details)
            error_response = error_handler(error_object)
            return make_response(error_response, 400)
        except ValueError as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_object = conflict(detail)
            error_response = error_handler(error_object)
            return make_response(error_response, 409)
        except Exception as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_object = internal_server_error(detail)
            error_response = error_handler(error_object)
            return make_response(error_response, 500)
