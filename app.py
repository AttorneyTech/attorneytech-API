from flask import Flask
from flask_restful import Api


from common.config import config_server
from resources.user import User


app = Flask(__name__)
api = Api(app)


api.add_resource(User, '/v1/users/<string:userId>')
app.run(
    port=config_server['port'],
    ssl_context=(config_server['cert_path'], config_server['key_path']),
    debug=True
)
