import psycopg2
import sys

from common.config import read_config


class DbConnection:
    '''
    Construct the connection of database
    '''
    def __init__(self):
        try:
            __config = read_config("database")
            __db_host = __config['db_host']
            __db_port = __config['port']
            __db_name = __config['db_name']
            __db_username = __config['db_username']
            __db_password = __config['db_password']
        except KeyError as e:
            print(f'KeyError: The key {e} in config file not found')
            sys.exit()

        self.__db_host = __db_host
        self.__db_port = __db_port
        self.__db_name = __db_name
        self.__db_username = __db_username
        self.__db_password = __db_password

    def connection(self):
        try:
            conn = psycopg2.connect(
                        host=self.__db_host,
                        port=self.__db_port,
                        dbname=self.__db_name,
                        user=self.__db_username,
                        password=self.__db_password
                    )
        except Exception as e:
            return e

        else:
            return conn
