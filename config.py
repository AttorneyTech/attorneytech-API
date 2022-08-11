import json


def read_config():
    '''
    Reading the configuration file
    '''
    with open('config.json', 'r') as config_f:
        config = json.load(config_f)

    return config
