import logging
import os
import sys
from datetime import datetime

from .config import read_config

sys.path.append("..")


config = read_config()
file_path = config['logging']['file_path']
folder_rotation = config['logging']['folder_rotation']
filename_rotation = config['logging']['filename_rotation']

log_folder = folder_rotation.format(datetime.now())
log_filename = filename_rotation.format(datetime.now())


def create_logger():
    formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%y/%m/%d %h:%m:%s'
                )
    api_logger = logging.getLogger()
    api_logger.setLevel(logging.DEBUG)

    if not os.path.exists(file_path + log_folder):
        os.makedirs(file_path + log_folder)

    file_handler = logging.FileHandler(
                        f'{file_path}{log_folder}/{log_filename}',
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
