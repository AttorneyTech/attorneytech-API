import json
import sys
import traceback


try:
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)

        api_config = config['api']
        db_config = config['database']
        logger_config = config['logger']

        api_host = api_config['hostname']
        api_port = api_config['port']

        db_port = db_config['port']
        db_host = db_config['host']
        db_name = db_config['db_name']
        db_username = db_config['username']
        db_password = db_config['password']

        logger_file_path = logger_config['file_path']
        logger_folder_name = logger_config['folder_name']
        logger_file_name = logger_config['file_name']
except Exception:
    traceback.print_exc()
    sys.exit()


class Config:
    def __init__(self):
        self.api_host = api_host
        self.api_port = api_port
        self.db_port = db_port
        self.db_host = db_host
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.logger_file_path = logger_file_path
        self.logger_folder_name = logger_folder_name
        self.logger_file_name = logger_file_name


config = Config()
