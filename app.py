from flask import Flask, abort
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)


class Users(Resource):
    def get(self, userId):
        for user in users:
            if user['data']['id'] == userId:
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
        if username == user['data']['attributes']['username']:
            if check_password_hash(
                user['data']['attributes']['password'],
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
    return f'Hello, {auth.current_user()}!'


api.add_resource(Users, '/users/<string:userId>')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
