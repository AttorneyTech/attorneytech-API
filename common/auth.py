from flask import make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from common.config import config_auth
from common.error_handler import Unauthorized
from common.logger import logger

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    '''
    Verify that the username and password combination.
    '''

    if (
        username == config_auth['username'] and
        check_password_hash(
            generate_password_hash(config_auth['password']), password
        )
    ):
        return username


@auth.error_handler
def auth_error():
    '''
    If failed authentication, send an authentication
    error back to the client.
    '''

    detail = (
        'Unauthorized. '
        'Username and password not matched with the Basic Auth credentials.'
    )
    error = Unauthorized(detail)
    logger.error(detail)

    return make_response(error.error_response(), 401)
