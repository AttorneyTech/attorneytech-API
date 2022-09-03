from datetime import datetime, timedelta
import logging
import logging.handlers
import os

from common.config import config


class Logger:
    '''
    Construct the logger object
    '''
    custom_tz = (
        datetime.utcnow() +
        timedelta(hours=config.logger_utc_offset)
    )

    def __init__(self):
        self.level = config.logger_level
        self.file_path = config.logger_file_path
        self.folder_name = config.logger_folder_name.format(
            Logger.custom_tz
        )
        self.file_name = config.logger_file_name.format(
            Logger.custom_tz
        )
        self.file_size_bytes = config.logger_file_size_bytes
        self.file_backup_count = config.logger_file_backup_count

    def create_logger(self):
        if not os.path.exists(f'{self.file_path}{self.folder_name}'):
            os.makedirs(f'{self.file_path}{self.folder_name}')

        # Logger format
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        datefmt = '%Y/%m/%d %H:%M:%S'

        # Basic config of logging
        logging.basicConfig(
            level=f'{self.level}',
            format=format,
            datefmt=datefmt
        )

        # Set file handler
        file_handler = logging.handlers.RotatingFileHandler(
            f'{self.file_path}{self.folder_name}'
            f'/{self.file_name}',
            mode='w',
            encoding='utf-8',
            maxBytes=self.file_size_bytes,
            backupCount=self.file_backup_count
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
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


logger = Logger().create_logger()
