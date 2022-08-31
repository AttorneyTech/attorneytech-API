from flask import Flask
from flask_restful import Api

from common.config import config
from resources.user import User


app = Flask(__name__)
api = Api(app)


app.config['JSON_SORT_KEYS'] = False


api.add_resource(User, '/v1/users/<string:userId>')
app.run(port=config.api_port, debug=True)
