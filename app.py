import psycopg2
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource

from config import read_config
from log import create_logger


# Initialize the flask framework
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

# Set the constants
config = read_config()
api_port = config['api']['port']
db_host = config['database']['db_host']
db_port = config['database']['port']
db_name = config['database']['db_name']
db_username = config['database']['db_username']
db_password = config['database']['db_password']


# Construct the connection to database
def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_username,
        password=db_password
    )
    return conn


class User(Resource):
    def get(self, userId):
        '''
        Get the specific user by user ID
        '''
        try:
            conn = get_db_connection()
        except Exception as response:
            response = jsonify({
                        "errors": [
                            {
                                "status": "500",
                                "title": "Internal Server Error",
                                "detail": "Can't connect to database"
                            }
                        ]
                    })
            api_logger.info('Can not connect to database')
            return make_response(response, 500)
        cur = conn.cursor()
        cur.execute(f'''
                    SELECT
                    users.id, users.role, users.username,
                    users.first_name, users.middle_name,
                    users.last_name,
                    events.id AS event_id,
                    cases.id AS cases_id,
                    users.email, users.phone, users.street_name,
                    users.district, users.city, users.zip_code
                    FROM users
                    LEFT JOIN cases
                    ON users.id=cases.client_id or users.id=cases.agent_id
                    LEFT JOIN events
                    ON cases.event_id=events.id
                    WHERE users.id={userId};
                    '''
                    )
        response = cur.fetchall()
        cur.close()
        conn.close()
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
                            "id": f"{userId}", "type": "users",
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
            response = jsonify({
                        "errors": [
                            {
                                "status": "404",
                                "title": "Not Found",
                                "detail": "Resource not found"
                            }
                        ]
                    })
            api_logger.info('Resource not found')
            return make_response(response, 404)


api.add_resource(User, '/users/<string:userId>')


if __name__ == '__main__':
    api_logger = create_logger()
    app.run(port=api_port)
