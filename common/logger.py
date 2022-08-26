import logging
import logging.handlers
import os
from datetime import datetime

from common.config import config


class Logger:
    '''
    Construct the logger object
    '''
    def __init__(self):
        self.level = config.logger_level
        self.file_path = config.logger_file_path
        self.folder_name = config.logger_folder_name.format(datetime.now())
        self.file_name = config.logger_file_name.format(datetime.now())
        self.file_size_bytes = config.logger_file_size_bytes
        self.file_backup_count = config.logger_file_backup_count

    def create_logger(self):
        if not os.path.exists(f'{self.file_path}{self.folder_name}'):
            os.makedirs(f'{self.file_path}{self.folder_name}')

        # Logger format
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        datefmt = '%Y/%m/%d %H:%M:%S'

        # Set file handler
        file_handler = logging.handlers.RotatingFileHandler(
            f'{self.file_path}{self.folder_name}'
            f'/{self.file_name}',
            mode='w',
            encoding='utf-8',
            maxBytes=self.file_size_bytes,
            backupCount=self.file_backup_count
        )
        formatter = logging.Formatter(format)
        file_handler.setFormatter(formatter)

        # Basic config of logging
        logging.basicConfig(
            level=f'{self.level}',
            format=format,
            datefmt=datefmt
        )

        # Set handler of console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Initialize the logger and add the handlers to it
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


logger = Logger().create_logger()
