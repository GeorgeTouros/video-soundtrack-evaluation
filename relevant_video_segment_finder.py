import pandas as pd
from utils.catalog_utils import purge_temp_folder
from db_handler.db_handler import DatabaseHandler
from sqlalchemy import exc
from media_manipulation.song_retrieval import extract_audio_chunks_from_video, find_songs_in_temp_dir, \
    get_previous_and_next_values, smooth_chunk_matches, ieob_tagging_for_chunk_matches, calculate_offset_diff
from media_manipulation.song_retrieval import create_match_ids_per_video_segment, flag_possible_errors, get_crop_timestamps
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-T", "--tempdir", help="local temporary directory")
parser.add_argument("-I", "--startindex", help="the starting id of the batch")
parser.add_argument("-i", "--endindex", help="the ending id of the batch")

args = parser.parse_args()

if __name__ == '__main__':
    try:
        db = DatabaseHandler('file_system_catalogs')
    except exc.OperationalError:
        db = DatabaseHandler()
        db.create_db('file_system_catalogs')
        db = DatabaseHandler('file_system_catalogs')

    db_connection = db.connection

    if not db.check_for_existing_tables('audio_video_matches'):
        db.execute_from_file('./db_handler/sql/create_audio_video_matches_table.sql')

    if args.tempdir:
        local_video_temp_dir = args.tempdir
    else:
        raise ValueError('No temp folder was provided.')

    if args.startindex:
        start_index = int(args.startindex)
    else:
        raise ValueError('No starting index was provided.')

    if args.endindex:
        end_index = int(args.endindex)
    else:
        raise ValueError('No ending index was provided.')

    video_paths = pd.read_sql_table('video_catalog', con=db_connection)

    video_paths = video_paths.loc[video_paths['id'].between(start_index,end_index)]

    for video_id in video_paths[video_paths['searched'] == 0]['id'].values:
        video_path = video_paths[video_paths['id'] == video_id]['full_path'].values[0]
        file_type = video_paths[video_paths['id'] == video_id]['file_type'].values[0]
        extract_audio_chunks_from_video(video_path, temp_dir=local_video_temp_dir)
        matches = find_songs_in_temp_dir(video_id, local_video_temp_dir)
        match_df = pd.DataFrame.from_records(matches, columns=['chunk', 'start', 'end', 'song_id',
                                                               'song_name', 'input_confidence', 'offset',
                                                               'offset_seconds'])
        match_df['start'] = match_df.start.astype('int')
        match_df['end'] = match_df.end.astype('int')
        match_df.sort_values(by='start', inplace=True)
        match_df = get_previous_and_next_values(match_df, ['song_id', 'offset_seconds'])
        match_df.sort_values(by='start', inplace=True)
        match_df['song_id'], match_df['offset_seconds'] = zip(*match_df.apply(func=smooth_chunk_matches, axis=1))
        match_df.sort_values(by='start', inplace=True)
        match_df = get_previous_and_next_values(match_df, ['song_id', 'offset_seconds'])
        match_df.sort_values(by='start', inplace=True)
        match_df['match_tag'] = match_df.apply(func=ieob_tagging_for_chunk_matches, axis=1)
        match_df.sort_values(by='start', inplace=True)
        match_df['offset_diff'] = match_df.apply(func=calculate_offset_diff, axis=1)
        match_df['match_id'] = create_match_ids_per_video_segment(match_df['match_tag'].values)
        match_df.sort_values(by='start', inplace=True)
        match_df = flag_possible_errors(match_df)
        match_df = match_df[match_df['too_small'] == 0]
        if len(match_df) > 0:
            trimmer_df = get_crop_timestamps(match_df)
            trimmer_df['video_type'] = file_type
            trimmer_df['video_id'] = video_id
            trimmer_df['real'] = 1
            trimmer_df = trimmer_df.drop(columns='match_id')
            trimmer_df = trimmer_df.rename(mapper={'song_id': 'djv_song_id'}, axis=1)

            video_clips = trimmer_df[['video_id', 'start', 'end', 'video_type']].drop_duplicates
            video_clips.to_sql('video_clips_catalog', con=db_connection, index=False, if_exists='append')

            vcc = pd.read_sql_table('video_clip_catalog', con=db_connection, index_col='id')
            vcc.rename(mapper={'id': 'clip_id'}, axis=1)

            joined = pd.merge(left=trimmer_df, right=vcc,
                              left_on=['video_id', 'start'], right_on=['video_id', 'start'],
                              how='inner')

            joined[['djv_song_id', 'invalid_mode', 'real', 'clip_id']].to_sql('audio_video_matches',
                                                                              con=db_connection,
                                                                              index=False,
                                                                              if_exists='append',
                                                                              method='multi')
        db.update_value(table_name='video_catalog',
                        column_name='searched',
                        value=1,
                        where="id = {}".format(video_id))
        purge_temp_folder(local_video_temp_dir)
        print('Completed work for ' + video_path)
