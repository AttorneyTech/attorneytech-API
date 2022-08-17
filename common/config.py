import json


def read_config_of_api():
    '''
    Reading the configuration file
    '''
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
        config_api = config["api"]

    return config_api


def read_config_of_db():
    '''
    Reading the configuration file
    '''
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
        config_db = config["database"]

    return config_db


def read_config_of_logger():
    '''
    Reading the configuration file
    '''
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
        config_logger = config["logger"]

    return config_logger
