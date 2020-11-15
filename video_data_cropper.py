import pandas as pd
from db_handler.db_handler import DatabaseHandler
import os
from utils.catalog_utils import get_collection_directory, setup_curated_video_dir
from sqlalchemy import exc
from math import floor
from media_manipulation.video_manipulation import video_chunker


if __name__ == '__main__':
    try:
        db = DatabaseHandler('file_system_catalogs')
    except exc.OperationalError:
        db = DatabaseHandler()
        db.create_db('file_system_catalogs')
        db = DatabaseHandler('file_system_catalogs')

    db_connection = db.connection

    with open('./sql/select_correct_videos.sql') as q_file:
        sql = q_file.read()
        vids = pd.read_sql(sql=sql, con=db_connection, index_col='id')

    vids['file_name'] = vids['video_audio_match_id'] + '_' + vids['start'].astype('str') + '.' + vids['video_type']

    video_path = get_collection_directory('video')
    os.chdir(video_path)

    target_dir = setup_curated_video_dir()

    vids['length'] = round(vids['end']/1000 - vids['start']/1000, 0)

    vids['no_of_vids'] = vids['length'].apply(lambda x: floor(x/15))

    vids['target'] = vids.apply(func=lambda row: video_chunker(row['file_name'], target_dir, '.mp4', row['length'], 15),
                                axis=1)

    print('Your work is done master.')
