import logging
import os
from datetime import datetime
from config import read_config
import sys
sys.path.append("..")


config = read_config()
FILE_PATH = config['logging']['file_path']
FOLDER_ROTATION = config['logging']['folder_rotation']
FILENAME_ROTATION = config['logging']['filename_rotation']

LOG_FOLDER = FOLDER_ROTATION.format(datetime.now())
LOG_FILENAME = FILENAME_ROTATION.format(datetime.now())


def create_logger():
    formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S'
                )
    api_logger = logging.getLogger()
    api_logger.setLevel(logging.DEBUG)

    if not os.path.exists(FILE_PATH + LOG_FOLDER):
        os.makedirs(FILE_PATH + LOG_FOLDER)

    file_handler = logging.FileHandler(
                        FILE_PATH + LOG_FOLDER + '/' + LOG_FILENAME,
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
