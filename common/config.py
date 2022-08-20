import json
import sys


def read_config(key):
    '''
    Reading the configuration file
    '''
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
        try:
            config = config[key]
        except KeyError as e:
            print(f'KeyError: The key {e} in config file not found')
            sys.exit()

    return config
