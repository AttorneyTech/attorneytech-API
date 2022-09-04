from datetime import datetime, timedelta
import logging
import logging.handlers
import os
import sys
import traceback

from common.config import config


# Get the configurations of logger
try:
    config_logger = config['logger']
    custom_tz = (
        datetime.utcnow() +
        timedelta(hours=config_logger['utc_offset'])
    )
    level = config_logger['level']
    file_path = config_logger['file_path']
    folder_name = config_logger['folder_name'].format(custom_tz)
    file_name = config_logger['file_name'].format(custom_tz)
    file_size_bytes = config_logger['file_size_bytes']
    file_backup_count = config_logger['file_backup_count']
except Exception:
    traceback.print_exc()
    sys.exit()


class Logger:
    '''
    Construct the logger object
    '''
    def create_logger(self):
        '''
        Create a logger and definite its format, config,
        handlers and formatter.
        '''
        if not os.path.exists(f'{file_path}{folder_name}'):
            os.makedirs(f'{file_path}{folder_name}')

        # Logger format
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        datefmt = '%Y/%m/%d %H:%M:%S'

        # Basic config of logging
        logging.basicConfig(
            level=f'{level}',
            format=format,
            datefmt=datefmt
        )

        # Set file handler
        file_handler = logging.handlers.RotatingFileHandler(
            f'{file_path}{folder_name}/{file_name}',
            mode='w',
            encoding='utf-8',
            maxBytes=file_size_bytes,
            backupCount=file_backup_count
        )

        # Set console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Custom the timezone of logger
        def custom_timezone(*args):
            tz = custom_tz
            return tz.timetuple()

        # Replace the default converter to custom converter
        logging.Formatter.converter = custom_timezone

        # Set the formatter
        formatter = logging.Formatter(format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Initialize the logger and add the handlers to it
        logger = logging.getLogger('API')
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger


logger = Logger().create_logger()
