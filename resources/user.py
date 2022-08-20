from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from werkzeug.security import check_password_hash
from db.user_verify_dao import UserVerifyDao

from common.error_handler import (
    NotFound, InternalServerError, UnauthorizedLogin
    )
from common.logger import Logger
from db.connection import DbConnection
from db.user_dao import UserDao
from models.user_model import UserModel


api_logger = Logger().create_logger()
connection = DbConnection()
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user_login = UserVerifyDao(username)
    user_login_data = user_login.get_data_from_db()

    if (user_login_data and
        username in user_login_data and
            check_password_hash(user_login_data.get(username), password)):

        return username


@auth.error_handler
def auth_error():
    error = UnauthorizedLogin()
    api_logger.error(error.detail)

    return make_response(error.error_response(), 401)


class User(Resource):
    @auth.login_required
    def get(self, userId):
        '''
        Get the specific user by user ID
        '''
        # Access data by user data access object

        user_dao = UserDao(userId)

        try:
            user_raw_data = user_dao.get_data_from_db()

        except Exception as e:
            # Parse error as string

            error_message_raw = str(e).split()
            error_message = ' '.join(
                    error_message_raw[:3] +
                    error_message_raw[8:9] +
                    error_message_raw[10:13]
                )

            error = InternalServerError(error_message)
            api_logger.error(error_message)

            return make_response(error.error_response(), 500)

        else:
            if user_raw_data:
                user_response_json_api = UserModel.serialize_user_data(
                                                user_raw_data, userId
                                            )
                api_logger.info('Successful response')

                return make_response(user_response_json_api, 200)
            else:
                error = NotFound()
                api_logger.error('Resource not found')

                return make_response(error.error_response(), 404)
