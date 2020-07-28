import sqlalchemy
from credentials import MySQL


class DatabaseHandler(object):
    _instance = None

    def __new__(cls, db_name=None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, db_name=None):
        self.user = MySQL['user']
        self.password = MySQL['password']
        self.host = MySQL['host']
        self.db_name = db_name
        self.connection = self.connect()

    def connect(self):
        try:
            print('connecting to MySQL database...')
            if self.db_name:
                engine = DatabaseHandler._instance.connection = sqlalchemy.create_engine(
                    'mysql://{0}:{1}@{2}/{3}'.format(self.user, self.password, self.host, self.db_name))
                connection = engine.connect()
            else:
                engine = DatabaseHandler._instance.connection = sqlalchemy.create_engine(
                    'mysql://{0}:{1}@{2}'.format(self.user, self.password, self.host))
                connection = engine.connect()
            print('connection established')
            return connection
        except Exception as error:
            print('Error: connection not established {}'.format(error))
            self._instance = None
            raise

    def query(self, query):
        try:
            result = self.connection.execute(query)
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def check_for_existing_dbs(self,):
        """
        Checks the available dbs in a MySQL server
        :param engine: the engine
        :return: a list of the existing dbs
        """
        existing_dbs = self.connection.execute("SHOW DATABASES;")
        existing_dbs = [d[0] for d in existing_dbs]
        return existing_dbs

    def create_db(self, db_name):
        """
        Checks if a db already exists in the server and if not creates it
        :param db_name: the name of the db that needs to be built
        :return: a success or fail message
        """
        if db_name not in self.check_for_existing_dbs():
            self.connection.execute("CREATE DATABASE {0}".format(db_name))
            print('Successfully created db {0}'.format(db_name))
        else:
            print('A database already exists with that name')

    def close(self):
        self.connection.close()

    def __del__(self):
        self.connection.close()
