import logging
import os
from datetime import datetime

from common.config import config


class Logger:
    '''
    Construct the logger object
    '''
    def __init__(self):
        self.file_path = config.logger_file_path
        self.folder_name = config.logger_folder_name.format(datetime.now())
        self.file_name = config.logger_file_name.format(datetime.now())

    def create_logger(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%y/%m/%d %h:%m:%s'
        )
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        if not os.path.exists(f'{self.file_path}{self.folder_name}'):
            os.makedirs(f'{self.file_path}{self.folder_name}')

        # file handler
        file_handler = logging.FileHandler(
            f'{self.file_path}{self.folder_name}'
            f'/{self.file_name}',
            'w',
            'utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger


logger = Logger().create_logger()
