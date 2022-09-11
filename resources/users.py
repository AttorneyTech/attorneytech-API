from flask import make_response
from flask_restful import Resource


from common.auth import auth
from common.error_handler import InternalServerError
from common.logger import logger
from db.users_dao import users_dao
from serializers.users_serializer import UserSerializer


class Users(Resource):
    @auth.login_required
    def get(self):
        '''
        Get the list of users
        '''
        try:
            filters = users_dao.get_filters()
            raw_user = users_dao.get_users(
                role=filters['role'],
                city=filters['city'],
                event_ids=filters['event_ids'],
                case_ids=filters['case_ids']
            )
            user_response_json = UserSerializer.serialize_raw_user(
                raw_user
            )
            return make_response(user_response_json, 200)
        except Exception as err:
            error = InternalServerError(
                str(err).replace('\"', '').replace('\n', '')
            )
            logger.error(err)
            return make_response(error.error_response(), 500)
