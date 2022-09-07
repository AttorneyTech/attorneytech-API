from flask import make_response
from flask_restful import Resource


from common.auth import auth
from common.error_handler import InternalServerError
from common.logger import logger
from db.users_dao import users_dao
from serializers.user_serializer import UserSerializer


class Users(Resource):
    @auth.login_required
    def get(self):
        '''
        Get the list of users
        '''
        pass
