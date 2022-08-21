import logging
import os
import sys

from datetime import datetime

from .config import read_config


class Logger:
    '''
    Construct the logger
    '''
    def __init__(self):
        try:
            __config = read_config("logger")
            __file_path = __config['file_path']
            __folder_rotation = __config['folder_rotation']
            __filename_rotation = __config['filename_rotation']
        except KeyError as e:
            print(f'KeyError: The key {e} in config file not found')
            sys.exit()

        self.file_path = __file_path
        self.folder_rotation = __folder_rotation
        self.filename_rotation = __filename_rotation
        self.log_folder = self.folder_rotation.format(datetime.now())
        self.log_filename = self.filename_rotation.format(datetime.now())

    def create_logger(self):
        formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%y/%m/%d %h:%m:%s'
                )
        api_logger = logging.getLogger()
        api_logger.setLevel(logging.DEBUG)

        if not os.path.exists(self.file_path + self.log_folder):
            os.makedirs(self.file_path + self.log_folder)

        file_handler = logging.FileHandler(
                            f'{self.file_path}{self.log_folder}'
                            f'/{self.log_filename}',
                            'w', 'utf-8'
                        )
        file_handler.setFormatter(formatter)
        api_logger.addHandler(file_handler)

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        api_logger.addHandler(console_handler)

        return api_logger
