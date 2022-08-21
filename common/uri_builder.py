#  apiBaseUrl, resourcePathLink, paramsLink
import sys

from .config import read_config


config = read_config('api')

try:
    hostname = config['host']
    port = config['port']
    version = 'v1'
except KeyError as e:
    print(f'KeyError: The key {e} in config file not found')
    sys.exit()


def uri_builder(resource_path):
    api_base_url = f'http://{hostname}:{port}/{version}'

    uri = f'{api_base_url}/{resource_path}'

    return uri
