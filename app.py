from flask import Flask
from flask_restful import Api

from common.config import read_config_of_api
from resources.user import User


# Initialize the flask framework
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

# Set the constants
config = read_config_of_api()
api_port = config['port']


api.add_resource(User, '/users/<string:userId>')


if __name__ == '__main__':
    app.run(port=api_port)
