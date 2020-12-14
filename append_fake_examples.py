import pandas as pd
from db_handler.db_handler import DatabaseHandler

if __name__ == '__main__':
    db = DatabaseHandler('file_system_catalogs')
    db_connection = db.connection
    fake = pd.read_csv('./var/fake_examples.csv')
    fake.to_sql('audio_video_matches', con=db_connection, index=False, if_exists='append', method='multi')