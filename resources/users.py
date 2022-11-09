import json

from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from common.auth import auth
from common.custom_exception import CustomValidationError
from common.error_handler import (
    bad_request,
    internal_server_error,
    error_names
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
            error_response, error_code = bad_request(details)
            return make_response(error_response, error_code)
        except Exception as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_response, error_code = internal_server_error(detail)
            return make_response(error_response, error_code)

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
            dao = UsersDao()
            raw_data = request.get_json()
            valid_data, case_ids = validate_post_user(dao, raw_data)
            raw_user_id = dao.post_user(valid_data)
            user_id = raw_user_id[0]
            if case_ids:
                dao.post_cases_users(case_ids, user_id)
            raw_user = dao.get_user_by_id(user_id)
            user_object = UsersSerializer.raw_user_serializer(raw_user)
            serialized_user = UsersSerializer.user_response(user_object)
            return make_response(serialized_user, 201)
        except ValidationError as err:
            details = []
            detail = error_detail_handler(
                json.dumps(err.messages, ensure_ascii=False)
            )
            details.append(detail)
            logger.error(details)
            error_response, error_code = bad_request(details)
            return make_response(error_response, error_code)
        except (CustomValidationError, Exception) as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            if type(err).__name__ in error_names.keys():
                error_handler = error_names[type(err).__name__]
            else:
                error_handler = internal_server_error
            error_response, error_code = error_handler(detail)
            return make_response(error_response, error_code)
