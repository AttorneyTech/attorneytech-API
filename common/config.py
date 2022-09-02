import json
import sys
import traceback


try:
    with open('common/config.json', 'r') as config_f:
        config = json.load(config_f)
        server_config = config['server']
        db_config = config['database']
        logger_config = config['logger']

        # Load config of server
        server_host = server_config['hostname']
        server_port = server_config['port']
        server_key = server_config['key_path']
        server_cert = server_config['cert_path']

        # Load config of database
        db_port = db_config['port']
        db_host = db_config['host']
        db_name = db_config['db_name']
        db_username = db_config['username']
        db_password = db_config['password']

        # Load config of logger
        logger_utc_offset = logger_config['utc_offset']
        logger_level = logger_config['level']
        logger_file_path = logger_config['file_path']
        logger_folder_name = logger_config['folder_name']
        logger_file_name = logger_config['file_name']
        logger_file_size_bytes = logger_config['file_size_bytes']
        logger_file_backup_count = logger_config['file_backup_count']
except Exception:
    traceback.print_exc()
    sys.exit()


class Config:
    def __init__(self):
        # server config
        self.server_host = server_host
        self.server_port = server_port
        self.server_key = server_key
        self.server_cert = server_cert

        # db config
        self.db_port = db_port
        self.db_host = db_host
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password

        # logger config
        self.logger_level = logger_level
        self.logger_utc_offset = logger_utc_offset
        self.logger_file_path = logger_file_path
        self.logger_folder_name = logger_folder_name
        self.logger_file_name = logger_file_name
        self.logger_file_size_bytes = logger_file_size_bytes
        self.logger_file_backup_count = logger_file_backup_count


config = Config()
