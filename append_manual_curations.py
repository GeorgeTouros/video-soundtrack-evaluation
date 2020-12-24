import pandas as pd
from db_handler.db_handler import DatabaseHandler

if __name__ == '__main__':
    db = DatabaseHandler('file_system_catalogs')
    db_connection = db.connection

    if not db.check_for_existing_tables('audio_video_match_curation'):
        db.execute_from_file('./db_handler/sql/create_audio_video_match_curation.sql')

    curated = pd.read_csv('./var/video_match_curation.csv')
    curated.to_sql('audio_video_match_curation', con=db_connection, index=False, if_exists='replace', method='multi')

    try:
        fake = pd.read_csv('./var/fake_examples.csv')
        fake.to_sql('audio_video_matches', con=db_connection, index=False, if_exists='append', method='multi')
    except FileNotFoundError:
        print("You need to manually create the fake_examples.csv and store it in ./var/")
