from config import read_config
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource
import psycopg2


# Initialize the flask framework
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)


# Set the constants
config = read_config()
API_PORT = config['API']['PORT']
DB_HOST = config['DATABASE']['DB_HOST']
DB_PORT = config['DATABASE']['PORT']
DB_NAME = config['DATABASE']['DB_NAME']
DB_USERNAME = config['DATABASE']['DB_USERNAME']
DB_PASSWORD = config['DATABASE']['DB_PASSWORD']


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


class User(Resource):
    def get(self, userId):
        conn = get_db_connection()
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
                    JOIN cases
                    ON users.id=cases.client_id
                    JOIN events
                    ON cases.event_id=events.id
                    WHERE users.id={userId};
                    '''
                    )
        response = cur.fetchall()
        cur.close()
        conn.close()
        if response:
            if len(response) > 1:
                events = []
                cases = []
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
                            },
                        },
                    })
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
            return make_response(response, 404)


api.add_resource(User, '/users/<string:userId>')


if __name__ == '__main__':
    app.run(port=API_PORT, debug=True)
