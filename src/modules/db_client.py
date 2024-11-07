import MySQLdb
from configparser import ConfigParser

from modules.log_client import LogClient

class DBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBClient, cls).__new__(cls)
        return cls._instance

    def init_connection(self):
        self._connected = False
        self._logger = LogClient()
        self._logger.log("Connecting to the database...", "info")
        
        config = ConfigParser()
        config.read('.env')
        db_config = {
            'host': config.get('local', 'DB_HOST'),
            'user': config.get('local', 'DB_USER'),
            'password': config.get('local', 'DB_PASS'),
            'database': config.get('local', 'DB_NAME'),
            'port': int(config.get('local', 'DB_PORT'))
        }
        
        try:
            self.connection = MySQLdb.connect(**db_config)
            self.cursor = self.connection.cursor()
            
            self._connected = True
            self._logger.log("Connected to the database successfully.", "info")
        except MySQLdb._exceptions.MySQLError as e:
            self._connected = False
            
            self._logger.log("Error connecting to database: {}".format(e), 'error')
            self._logger.log("Launch application again.", "error")

    @property
    def connected(self):
        return self._connected