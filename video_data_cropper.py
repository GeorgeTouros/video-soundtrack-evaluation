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
        raise exc.OperationalError("You're impatient! First run inventory_catalogs_and_matching.py")

    db_connection = db.connection

    with open('db_handler/sql/select_correct_videos.sql') as q_file:
        sql = q_file.read()
        vids = pd.read_sql(sql=sql, con=db_connection, index_col='id')
    # get input absolute path
    vids['input_name'] = vids['directory'] + '/' + vids['filename']
    # create the result title
    vids['target_name'] = 'V' + vids.index.astype('str') + '_' + vids['start'].astype('str') + '.' + vids['video_type']

    video_path = get_collection_directory('video')
    os.chdir(video_path)

    target_dir = video_path

    vids['length'] = round(vids['end'] / 1000 - vids['start'] / 1000, 0)

    vids['no_of_vids'] = vids['length'].apply(lambda x: floor(x / 15))

    vids.apply(func=lambda row: video_chunker(input_file=row['input_name'],
                                              target_directory=target_dir,
                                              target_name=row['target_name'],
                                              file_type='.mp4',
                                              file_length=row['length'],
                                              chunk_size=row['length'],
                                              start=row['start']),
               axis=1)

    print('Your work is done master.')
