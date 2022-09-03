import sys
import traceback
from common.config import config


# Get the configurations of server
try:
    config_server = config['server']
    hostname = config_server['hostname']
    port = config_server['port']
    version = 'v1'
except Exception:
    traceback.print_exc()
    sys.exit()


def uri_builder(resource_path):
    api_base_url = f'https://{hostname}:{port}/{version}'
    uri = f'{api_base_url}/{resource_path}'

    return uri
