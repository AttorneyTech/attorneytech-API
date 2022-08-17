from flask import jsonify, make_response
from flask_restful import Resource

from common.logger import Logger
from common.error_handler import NotFound
from db.connection import DbConnection
from db.user_dao import UserDao

api_logger = Logger().create_logger()
connection = DbConnection()



class User(Resource):
    def get(self, userId):
        '''
        Get the specific user by user ID
        '''
        user_dao = UserDao(userId)
        response = user_dao.get_data_from_db()

        # try:
        #     conn = connection.connection()
        # except Exception as e:
        #     error_message = str(e)
        #     error = InternalServerError(error_message)
        #     api_logger.info(error_message)
        #     return make_response(error.error_response(), 500)
        # cur = conn.cursor()
        # cur.execute(f'''
        #             SELECT
        #             users.id AS user_id,
        #             users.role,
        #             users.username,
        #             users.first_name,
        #             users.middle_name,
        #             users.last_name,
        #             events.id AS event_id,
        #             cases.id AS cases_id,
        #             users.email,
        #             users.phone,
        #             users.street_name,
        #             users.district,
        #             users.city,
        #             users.zip_code
        #             FROM users
        #             LEFT JOIN cases
        #             ON users.id=cases.client_id or users.id=cases.agent_id
        #             LEFT JOIN events
        #             ON cases.event_id=events.id
        #             WHERE users.id={userId};
        #             '''
        #             )
        # response = cur.fetchall()
        # cur.close()
        # conn.close()
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
