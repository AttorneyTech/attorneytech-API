from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

from common.auth import auth
from common.custom_exception import CustomBadRequestError, CustomConflictError
from common.dict_handler import get_marshmallow_valid_message
from common.error_handler import (
    bad_request,
    internal_server_error,
    user_not_found,
    error_names
)
from common.logger import logger
from common.string_handler import error_detail_handler
from common.validate_data import validate_user_data
from db.users_dao import UsersDao
from serializers.users_serializer import UsersSerializer


class User(Resource):
    @auth.login_required
    def get(self, user_id):
        '''Get the specific user data by user ID'''

        try:
            dao = UsersDao
            if not user_id.isdigit():
                error_response, error_code, detail = user_not_found(user_id)
                logger.error(detail)
                return make_response(error_response, error_code)

            raw_user = dao.get_user_by_id(self, user_id)

            if raw_user:
                user_object = UsersSerializer.raw_user_serializer(raw_user)
                serialized_user = UsersSerializer.user_response(user_object)
                return make_response(serialized_user, 200)
            else:
                error_response, error_code, detail = user_not_found(user_id)
                logger.error(detail)
                return make_response(error_response, error_code)
        except Exception as err:
            detail = error_detail_handler(err)
            logger.error(detail)
            error_response, error_code = internal_server_error(detail)
            return make_response(error_response, error_code)

    def patch(self, user_id):
        '''Update information for a user by ID'''

        try:
            dao = UsersDao()
            raw_data = request.get_json()
            valid_data, case_ids = validate_user_data(
                dao, raw_data, patch=True
            )

            attributes = valid_data.get('data').get('attributes')

            if 'caseIds' in attributes.keys():
                dao.patch_cases_users(case_ids, user_id)

            dao.patch_user(valid_data, user_id)
            raw_user = dao.get_user_by_id(user_id)
            user_object = UsersSerializer.raw_user_serializer(raw_user)
            serialized_user = UsersSerializer.user_response(user_object)
            return make_response(serialized_user, 200)
        except (ValidationError, CustomBadRequestError) as err:
            details = []

            if type(err).__name__ == 'ValidationError':
                messages = get_marshmallow_valid_message(
                    data=err.messages, values=[]
                )
                details = [error_detail_handler(detail) for detail in messages]
            else:
                detail = error_detail_handler(err)
                details.append(detail)

            logger.error(details)
            error_response, error_code = bad_request(details)
            return make_response(error_response, error_code)
        except (CustomConflictError, Exception) as err:
            detail = error_detail_handler(err)
            logger.error(detail)

            if type(err).__name__ in error_names.keys():
                error_handler = error_names[type(err).__name__]
            else:
                error_handler = internal_server_error

            error_response, error_code = error_handler(detail)
            return make_response(error_response, error_code)
