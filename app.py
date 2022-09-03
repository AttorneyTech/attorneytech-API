import sys
import traceback

from flask import Flask
from flask_restful import Api

from common.config import config
from resources.user import User


# Get the configurations of server
try:
    config_server = config['server']
    port = config_server['port']
    key = config_server['key_path']
    cert = config_server['cert_path']
except Exception:
    traceback.print_exc()
    sys.exit()

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


api.add_resource(User, '/v1/users/<string:userId>')
app.run(
    port=port,
    ssl_context=(cert, key),
    debug=True
)
