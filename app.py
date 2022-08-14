import psycopg2
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from config import read_config
from logs.log import create_logger

# Initialize the flask framework
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)


# Set the constants
config = read_config()
API_PORT = config['api']['port']
DB_HOST = config['database']['db_host']
DB_PORT = config['database']['port']
DB_NAME = config['database']['db_name']
DB_USERNAME = config['database']['db_username']
DB_PASSWORD = config['database']['db_password']


# Construct the connection to database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
    return conn


class Users(Resource):
    @staticmethod
    def get_filter():
        role = request.args.get('filter[role]')
        city = request.args.get('filter[city]')
        eventIds = request.args.get('filter[eventIds]')
        caseIds = request.args.get('filter[caseIds]')
        query_params = {

            'role': role, 'city': city,
            'eventIds': eventIds, 'caseIds': caseIds

            }
        return query_params

    def get(self):
        '''
        Get the list of users
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
        cur.execute('SELECT users.id FROM users;')
        response = cur.fetchall()
        cur.close()

        # Get the id list of users
        users_id_list = []
        for row in range(len(response)):
            users_id_list.append(response[row][0])
        # Create data list of users
        users_data = []
        for userId in users_id_list:
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
            if response:
                events, cases = [], []
                for row in response:
                    if str(row[6]) not in events:
                        events.append(str(row[6]))
                    cases.append(str(row[7]))
                user_dict = {
                                "id": f"{userId}", "type": "users",
                                "links": {
                                    "self":
                                        f"http://127.0.0.1:5000/users/{userId}"
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
                                },
                            }
                query_params = Users.get_filter()
                is_target_data = True
                for key, value in query_params.items():
                    if not value:
                        continue
                    elif (
                            key == 'role' and
                            user_dict['attributes'][key] != value
                            ):
                        is_target_data = False
                    elif (
                            key == 'city' and
                            user_dict['attributes']['address'][key] != value
                            ):
                        is_target_data = False
                    elif (
                            key == 'eventIds'
                            and value not in user_dict['attributes'][key]
                            ):
                        is_target_data = False
                    elif (
                            key == 'caseIds' and
                            value not in user_dict['attributes'][key]
                            ):
                        is_target_data = False
                if is_target_data:
                    users_data.append(user_dict)
        response = jsonify({
                        "links": {
                            "self": "http://127.0.0.1:5000/users"
                        },
                        "data": users_data
                    })
        api_logger.info('Successful response')
        return make_response(response, 200)


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


api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:userId>')


if __name__ == '__main__':
    api_logger = create_logger()
    app.run(port=API_PORT, debug=True)
