from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from werkzeug.security import check_password_hash


from common.error_handler import (
    NotFound, InternalServerError, UnauthorizedLogin
    )
from common.logger import Logger
from db.connection import DbConnection
from db.user_dao import UserDao
from db.user_verify_dao import UserVerifyDao
from serializers.user_serializer import UserSerializer


api_logger = Logger().create_logger()
connection = DbConnection()
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user_login = UserVerifyDao(username)
    user_login_data = user_login.verify_user_from_db()

    # Set the variable 'login_internal_error'
    # for the use of auth_error() function

    global login_internal_error
    login_internal_error = None

    # If the user_login_data is a error message,
    # put it into a 'login_internal_error' variable

    if type(user_login_data) is str:
        login_internal_error = user_login_data

    # Check if the login data is valid

    elif (user_login_data and
            username in user_login_data and
            check_password_hash(user_login_data.get(username), password)):

        return username


@auth.error_handler
def auth_error():
    if login_internal_error:
        err = login_internal_error
        error = InternalServerError(err)
        api_logger.error(err)

        return make_response(error.error_response(), 500)
    else:
        error = UnauthorizedLogin()
        api_logger.error(error.detail)

        return make_response(error.error_response(), 401)


class User(Resource):
    @auth.login_required
    def get(self, userId):
        '''
        Get the specific user data by user ID
        '''
        user_dao = UserDao(userId)
        user_raw_data = user_dao.get_user_by_id()

        # If user_raw_data
        if type(user_raw_data) is str:
            err = user_raw_data
            error = InternalServerError(err)
            api_logger.error(err)

            return make_response(error.error_response(), 500)

        elif user_raw_data:
            user_response_json_api = UserSerializer.serialize_user_data(
                                                user_raw_data, userId
                                            )
            api_logger.info('Successful response')

            return make_response(user_response_json_api, 200)

        else:
            error = NotFound(userId)
            api_logger.error('Resource not found')

            return make_response(error.error_response(), 404)
