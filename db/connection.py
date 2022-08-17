import psycopg2
from common.config import read_config


class DbConnection:
    '''
    Construct the connection of database
    '''
    def __init__(self):
        __config = read_config("database")
        self.__db_host = __config['db_host']
        self.__db_port = __config['port']
        self.__db_name = __config['db_name']
        self.__db_username = __config['db_username']
        self.__db_password = __config['db_password']

    def connection(self):
        conn = psycopg2.connect(
                    host=self.__db_host,
                    port=self.__db_port,
                    dbname=self.__db_name,
                    user=self.__db_username,
                    password=self.__db_password
                )
        return conn
