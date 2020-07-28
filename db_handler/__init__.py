import sqlalchemy
from credentials import MySQL

user = MySQL['user']
password = MySQL['password']
host = MySQL['host']

engine = sqlalchemy.create_engine('mysql://{0}:{1}@{2}'.format(user, password, host))


def check_for_existing_dbs(engine=engine):
    """
    Checks the available dbs in a MySQL server
    :param engine: the engine
    :return: a list of the existing dbs
    """
    existing_dbs = engine.execute("SHOW DATABASES;")
    existing_dbs = [d[0] for d in existing_dbs]
    return existing_dbs


def create_db(db_name):
    """
    Checks if a db already exists in the server and if not creates it
    :param db_name: the name of the db that needs to be built
    :return: a success or fail message
    """
    if db_name not in check_for_existing_dbs():
        engine.execute("CREATE DATABASE {0}".format(db_name))
        print('Successfully created db {0}'.format(db_name))
    else:
        print('A database already exists with that name')
