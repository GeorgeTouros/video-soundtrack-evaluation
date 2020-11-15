from dejavu import Dejavu
from config.credentials import MySQL
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

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


def get_fingerprints_from_file(file, song_name):
    djv.fingerprint_file(file_path=file, song_name=song_name)
    print("fingerprint done")


def ask_dejavu(audio_file):
    song = djv.recognize(FileRecognizer, audio_file)
    return song

def find_song_id_in_fingerprint_db(song_name):
    pass

def delete_song_from_fingerprint_db(song_id):
    pass