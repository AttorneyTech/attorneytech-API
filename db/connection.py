import sys

import psycopg2

from common.config import read_config


class DbConnection:
    '''
    Construct the connection of database
    '''
    def __init__(self):
        try:
            # Unnecessary private
            __config = read_config("database")
            self.__db_host = __config['db_host']
            self.__db_port = __config['port']
            self.__db_name = __config['db_name']
            self.__db_username = __config['db_username']
            self.__db_password = __config['db_password']
        except KeyError as e:
            print(f'KeyError: The key {e} in config file not found')
            sys.exit()

    # Get the connection to postgreSQL
    # If failed, return the error message
    def get_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.__db_host,
                port=self.__db_port,
                dbname=self.__db_name,
                user=self.__db_username,
                password=self.__db_password
            )
            raise 'error'
            return conn
        except BaseException as err:
            print('***********')
            print(err)
            print('***********')
        except Exception as err:

            return str(err).replace('\"', '').replace('\n', '')
