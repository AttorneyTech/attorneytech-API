from flask import jsonify, make_response
from flask_restful import Resource

from common.logger import Logger
from common.error_handler import NotFound, InternalServerError
from db.connection import DbConnection
from db.user_dao import UserDao

api_logger = Logger().create_logger()
connection = DbConnection()


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user by user ID
        '''
        # Access data by UserDao
        user_dao = UserDao(userId)

        try:
            response = user_dao.get_data_from_db()
        except Exception as e:
            error_message_raw = str(e).split()
            error_message = ' '.join(
                    error_message_raw[:3] +
                    error_message_raw[8:9] +
                    error_message_raw[10:13]
                )
            error = InternalServerError(error_message)
            api_logger.error(error_message)
            return make_response(error.error_response(), 500)

        if response:
            events, cases = [], []
            for row in response:
                if str(row[6]) not in events:
                    events.append(str(row[6]))
                cases.append(str(row[7]))
            response = jsonify({
                        "links": {
                            "self": f"http://127.0.0.1:5000/users/{userId}"
                        },
                        "data": {
                            "id": f'{userId}', "type": "users",
                            "links": {
                                "self": f"http://127.0.0.1:5000/users/{userId}"
                            },
                            "attributes": {
                                "role": response[0][1],
                                "username": response[0][2],
                                "firstName": response[0][3],
                                "middleName": response[0][4],
                                "lastName": response[0][5],
                                "eventIds": events,
                                "caseIds": cases,
                                "email": response[0][8],
                                "phone": response[0][9],
                                "address": {
                                    "addressLine1": response[0][10],
                                    "addressLine2": response[0][11],
                                    "city": response[0][12],
                                    "zipCode": response[0][13]
                                }
                            }
                        }
                    })
            api_logger.info('Successful response')
            return make_response(response, 200)
        else:
            error = NotFound()
            api_logger.error('Resource not found')
            return make_response(error.error_response(), 404)
