from dejavu import Dejavu
from credentials import MySQL

config = {
     "database": {
         "host": MySQL['host'],
         "user": MySQL['user'],
         "password": MySQL['password'],
         "database": "dejavu",
     }
 }
djv = Dejavu(config)


def get_fingerprints_from_directory(directory, file_types, no_of_processes=4):
    djv.fingerprint_directory(directory, file_types, no_of_processes)
    print("fingerprinting db is ready.")
