from flask import Flask, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api


app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)


users = [{
                "links": {
                    "self": "string"
                },
                "data": {
                    "id": '123',
                    "type": "users",
                    "links": {
                        "self": "string"
                    },
                    "attributes": {
                        "role": "agent",
                        "username": "saulgoodman2002",
                        "firstName": "研介",
                        "middleName": "string",
                        "lastName": "古美門",
                        "eventIds": [
                            "231",
                            "478"
                        ],
                        "caseIds": [
                            "47",
                            "30"
                        ],
                        "email": "saul.goodman@gmail.com",
                        "phone": "0911123456",
                        "address": {
                            "addressLine1": "西園路一段 200 號 8 樓",
                            "addressLine2": "萬華區",
                            "city": "臺北市",
                            "zipCode": "108"
                        },
                        "password": generate_password_hash("zoodagigi")
                    }
                }
                }]


class Users(Resource):
    def get(self, userId):
        for user in users:
            if user["data"]["id"] == userId:
                app.logger.info(
                    'The request of userId: %s successfully response',
                    userId
                )
                return user
        app.logger.info(
            'The request of userId: %s is not found',
            userId
        )
        return abort(404)


@auth.verify_password
def verify_password(username, password):
    for user in users:
        if username == user["data"]["attributes"]["username"]:
            if check_password_hash(
                user["data"]["attributes"]["password"],
                password
            ):
                app.logger.info('%s successfully logging', username)
                return username
            else:
                app.logger.info('%s is fail logging', username)
                abort(401)


@app.route('/')
@auth.login_required
def index():
    return f"Hello, {auth.current_user()}!"


api.add_resource(Users, "/users/<string:userId>")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
