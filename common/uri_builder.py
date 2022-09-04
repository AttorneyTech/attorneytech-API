from common.config import config_server


def uri_builder(resource_path):
    api_base_url = (
        f'https://{config_server["hostname"]}:'
        f'{config_server["port"]}/'
        f'{config_server["api_version"]}'
    )
    uri = f'{api_base_url}/{resource_path}'

    return uri
