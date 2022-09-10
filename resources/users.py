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



    # def get_filter():
    #     role = request.args.get('filter[role]')
    #     city = request.args.get('filter[city]')
    #     eventIds = request.args.get('filter[eventIds]')
    #     caseIds = request.args.get('filter[caseIds]')
