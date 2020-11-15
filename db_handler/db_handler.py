import sqlalchemy
from config.credentials import MySQL


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

    def update_value(self, table_name, column_name, value, where):
        """
        Updates a table with a given value based on column name and a where clause
        :param table_name:
        :param column_name:
        :param value:
        :param where:
        """
        update = "UPDATE {}\n".format(table_name)
        set_command = "SET {} = {}\n".format(column_name, value)
        where_clause = "WHERE {};".format(where)
        self.connection.execute(update+set_command+where_clause)

    def execute_from_file(self, filepath):
        """
        reads a file with sql code and executes it
        :param filepath:
        :return:
        """
        with open(filepath) as query_file:
            query = query_file.read()
            self.connection.execute(str(query))

    def check_for_existing_tables(self, table):
        """
        Checks the available tables in a MySQL db
        :return: a list of the existing dbs
        """
        existing_tables = self.connection.execute("SHOW TABLES;")
        existing_tables = [d[0] for d in existing_tables]
        if table in existing_tables:
            return True
        else:
            return False

    def close(self):
        self.connection.close()

    def __del__(self):
        self.connection.close()
