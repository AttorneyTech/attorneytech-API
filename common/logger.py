from datetime import datetime, timedelta
import logging
import logging.handlers
import os

from common.config import config_logger


class Logger:
    '''
    Construct the logger object
    '''
    # Custom your timezone
    custom_tz = (
        datetime.utcnow() +
        timedelta(hours=config_logger['utc_offset'])
    )

    log_path = (
        config_logger["file_path"] +
        config_logger["folder_name"].format(custom_tz) + '/'
    )

    log_file_name = (
        config_logger["file_name"].format(custom_tz)
    )

    def create_logger(self):
        '''
        Create a logger and definite its format, config,
        handlers and formatter.
        '''
        if not os.path.exists(Logger.log_path):
            os.makedirs(Logger.log_path)

        # Basic config of logging
        logging.basicConfig(
            level=config_logger["level"],
            format=config_logger['format'],
            datefmt=config_logger['date_format']
        )

        # Set file handler
        file_handler = logging.handlers.RotatingFileHandler(
            Logger.log_path + Logger.log_file_name,
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
        formatter = logging.Formatter(config_logger['format'])
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Initialize the logger and add the handlers to it
        logger = logging.getLogger('API')
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


logger = Logger().create_logger()
