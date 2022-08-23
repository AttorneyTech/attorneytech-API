import sys

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

from common.config import read_config
from resources.user import User


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
app.config['JSON_SORT_KEYS'] = False


config = read_config("api")

try:
    api_port = config['port']
except KeyError as e:
    print(f'KeyError: The key {e} in config file not found')
    sys.exit()

api.add_resource(User, '/v1/users/<string:userId>')
app.run(port=api_port, debug=True)
