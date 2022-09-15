from flask import Flask
from flask_restful import Api

from common.config import config_server
from resources.user import User
from resources.users import Users

app = Flask(__name__)
api = Api(app)
app.json.sort_keys = False

users_endpoint = f'/{config_server["api_version"]}/users'
api.add_resource(User, f'{users_endpoint}/<string:user_id>')
api.add_resource(Users, f'{users_endpoint}')
app.run(
    port=config_server['port'],
    ssl_context=(config_server['cert_path'], config_server['key_path']),
    debug=True
)
