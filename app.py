from flask import Flask
from flask_restful import Api

from common.config import read_config
from resources.user import User


app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


config = read_config("api")
api_port = config['port']


api.add_resource(User, '/users/<string:userId>')


if __name__ == '__main__':
    app.run(port=api_port, debug=True)
