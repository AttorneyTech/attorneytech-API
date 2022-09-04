from datetime import datetime, timedelta
import logging
import logging.handlers
import os

from common.config import config_logger


class Logger:
    '''
    Construct the logger object
    '''
    custom_tz = (
        datetime.utcnow() +
        timedelta(hours=config_logger['utc_offset'])
    )

    def create_logger(self):
        '''
        Create a logger and definite its format, config,
        handlers and formatter.
        '''
        if not os.path.exists(
            f'{config_logger["file_path"]}/'
            f'{config_logger["folder_name"].format(Logger.custom_tz)}'
        ):
            os.makedirs(
                f'{config_logger["file_path"]}/'
                f'{config_logger["folder_name"].format(Logger.custom_tz)}'
            )

        # Logger format
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        datefmt = '%Y/%m/%d %H:%M:%S'

        # Basic config of logging
        logging.basicConfig(
            level=f'{config_logger["level"]}',
            format=format,
            datefmt=datefmt
        )

        # Set file handler
        file_handler = logging.handlers.RotatingFileHandler(
            f'{config_logger["file_path"]}/'
            f'{config_logger["folder_name"].format(Logger.custom_tz)}/'
            f'{config_logger["file_name"].format(Logger.custom_tz)}',
            mode='w',
            encoding='utf-8',
            maxBytes=config_logger['file_size_bytes'],
            backupCount=config_logger['file_backup_count']
        )

        # Set console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Custom the timezone of logger
        def custom_timezone(*args):
            tz = Logger.custom_tz
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
