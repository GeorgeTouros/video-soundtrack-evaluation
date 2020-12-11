# Include standard modules
import argparse
from db_handler.db_handler import DatabaseHandler
from mysql.connector.errors import ProgrammingError
from utils.catalog_utils import get_collection_directory, purge_temp_folder

try:
    from fingerprinting import djv
except ProgrammingError:
    db = DatabaseHandler()
    db.create_db('dejavu')
    from fingerprinting import djv
import gc

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("-T", "--tempdir", help="local temporary directory")


args = parser.parse_args()


if __name__ == '__main__':
    if args.tempdir:
        local_audio_temp_dir = args.tempdir
        print("start making fingerprints")
        djv.get_fingerprints_from_directory(local_audio_temp_dir, ['wav'], 1)
        purge_temp_folder(local_audio_temp_dir)
        gc.collect()
    else:
        raise ValueError('No value was given for temp dir.')