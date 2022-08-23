from common.config import config


hostname = config.api_host
port = config.api_port
version = 'v1'


def uri_builder(resource_path):
    api_base_url = f'http://{hostname}:{port}/{version}'

    uri = f'{api_base_url}/{resource_path}'

    return uri
