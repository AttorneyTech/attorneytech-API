from common.config import config


hostname = config.server_host
port = config.server_port
version = 'v1'


def uri_builder(resource_path):
    api_base_url = f'https://{hostname}:{port}/{version}'

    uri = f'{api_base_url}/{resource_path}'

    return uri
