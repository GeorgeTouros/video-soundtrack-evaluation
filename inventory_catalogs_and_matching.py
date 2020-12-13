import re
import argparse
import pandas as pd
from mysql.connector.errors import ProgrammingError
from sqlalchemy import exc

from config.paths import audio_path, video_path, midi_path
from db_handler.db_handler import DatabaseHandler
from utils.catalog_utils import create_catalog, cleanup_file_titles, setup_collection_directory
from utils.catalog_utils import get_clean_song_titles_from_spotify, collect_matched_files
from utils.common_utils import script_start_time, script_run_time

try:
    from fingerprinting import djv
except ProgrammingError:
    db = DatabaseHandler()
    db.create_db('dejavu')
    from fingerprinting import djv

# set pandas print_options for debugging purposes
pd.options.display.width = 0

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mode", help="""Which part of the pipeline you need to run? 
                                            Choose between:\n all,\n midi,\n audio,\n merge""")

args = parser.parse_args()

if __name__ == '__main__':
    acceptable_modes = ['all', 'midi', 'audio', 'video', 'merge']

    if args.mode in acceptable_modes:
        mode = args.mode
        print('Running in {} mode'.format(mode))
        script_start_time()
    else:
        raise ValueError("Please provide a valid value for --mode")
    # we will remove the windows hidden files
    irrelevant_files = re.compile('(desktop\.ini)|(.*\.(jpg|db|txt|url|srt|info|nfo))')

    try:
        db = DatabaseHandler('file_system_catalogs')
    except exc.OperationalError:
        print('No such DB found. Setting up the Database')
        db = DatabaseHandler()
        db.create_db('file_system_catalogs')
        db = DatabaseHandler('file_system_catalogs')

        db_connection = db.connection

    if mode in ["midi", "all"]:
        # start with the midi files
        print('starting midi catalog')
        # Each midi file also has an indexing file that starts with .-
        # We remove those
        irrelevant_midi = re.compile('\._|\.DS_Store')
        irrelevant_dir = ['lmd_matched', 'cariart', 'download-midi']
        midi_catalog = create_catalog(midi_path, irrelevant_dir, irrelevant_midi)
        print('finish initial midi catalog')

        # clean -up the midi title names
        print('start midi catalog cleanup')
        if not db.check_for_existing_tables('midi_catalog'):
            db.execute_from_file('./db_handler/sql/create_midi_catalog.sql')
        midi_catalog = cleanup_file_titles(midi_catalog, "midi", allow_numbers=True)
        midi_catalog = get_clean_song_titles_from_spotify(midi_catalog)
        midi_catalog.drop_duplicates(inplace=True)
        try:
            already_there = pd.read_sql_table('midi_catalog', con=db_connection)
            midi_catalog = midi_catalog.loc[~midi_catalog['filename'].isin(already_there['filename'])]
            midi_catalog.to_sql('midi_catalog', con=db_connection, if_exists='append', index=False, index_label='id')
        except ValueError:
            midi_catalog.to_sql('midi_catalog', con=db_connection, if_exists='append', index=False, index_label='id')

        matches = midi_catalog[midi_catalog['spotify_name'].notna()]
        recall = 100 * len(matches) / len(midi_catalog)
        print('The recall is %i per cent' % recall)
        # TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

    if mode in ["audio", "all"]:
        # continue with the audio files
        print('start audio catalog')
        if not db.check_for_existing_tables('audio_catalog'):
            db.execute_from_file('./db_handler/sql/create_audio_catalog.sql')
        audio_catalog = create_catalog(audio_path, except_file=irrelevant_files, except_dir=['Bootlegs'])
        audio_catalog = cleanup_file_titles(audio_catalog, "audio")
        audio_catalog = get_clean_song_titles_from_spotify(audio_catalog)
        audio_catalog.drop_duplicates(inplace=True)
        try:
            already_there = pd.read_sql_table('audio_catalog', con=db_connection)
            audio_catalog = audio_catalog.loc[~audio_catalog['filename'].isin(already_there['filename'])]
            audio_catalog.to_sql('audio_catalog', con=db_connection, if_exists='append', index=False, index_label='id')
        except ValueError:
            audio_catalog.to_sql('audio_catalog', con=db_connection, if_exists='append', index=False, index_label='id')
        print('finish audio catalog')

    if mode in ['video', 'all']:
        # continue with the video files
        if not db.check_for_existing_tables('video_catalog'):
            db.execute_from_file('./db_handler/sql/create_video_catalog.sql')
        print('start video catalog')
        video_catalog = create_catalog(video_path, except_file=irrelevant_files)
        video_catalog = cleanup_file_titles(video_catalog, "video", allow_numbers=True)
        video_catalog['full_path'] = video_catalog['directory'] + '/' + video_catalog['filename']
        video_catalog['searched'] = 0
        try:
            already_there = pd.read_sql_table('video_catalog', con=db_connection)
            video_catalog = video_catalog.loc[~video_catalog['filename'].isin(already_there['filename'])]
            video_catalog.to_sql('video_catalog', con=db_connection, if_exists='append', index=False, index_label='id')
        except ValueError:
            video_catalog.to_sql('video_catalog', con=db_connection, if_exists='append', index=False, index_label='id')

        print('finish video catalog')

    if mode in ['merge', 'all']:
        print('Loading tables')
        if not db.check_for_existing_tables('midi_audio_matches'):
            db.execute_from_file('./db_handler/sql/create_audio_video_matches_table.sql')
        midi = pd.read_sql_table('midi_catalog', con=db_connection)
        audio = pd.read_sql_table('audio_catalog', con=db_connection)
        pos_midi = midi[midi['spotify_name'].notna()]
        pos_audio = audio[audio['spotify_name'].notna()]
        print('keep matches and drop duplicates')
        merged = pos_midi.merge(right=pos_audio, how='inner', on='spotify_URL', suffixes=('_midi', '_audio'))
        merged.drop_duplicates(subset='spotify_URL', inplace=True)
        print('creating the directories to store files')
        new_midi_dir, new_audio_dir, new_video_dir = setup_collection_directory()
        print('directories created successfully')
        print('collecting the files')
        merged['pair_id'] = merged.apply(collect_matched_files, new_midi_path=new_midi_dir,
                                         new_audio_path=new_audio_dir, axis=1)
        merged['djv_song_id'] = 'null'
        print('writing to db')
        try:
            already_there = pd.read_sql_table('midi_audio_matches', con=db_connection)
            merged = merged.loc[~merged['pair_id'].isin(already_there['pair_id'])]
            merged[['pair_id', 'index_midi', 'index_audio', 'djv_song_id']].to_sql('midi_audio_matches',
                                                                                   con=db_connection,
                                                                                   index=False,
                                                                                   if_exists='append')
        except ValueError:
            merged[['pair_id', 'index_midi', 'index_audio', 'djv_song_id']].to_sql('midi_audio_matches',
                                                                                   con=db_connection,
                                                                                   index=False,
                                                                                   if_exists='append')

    script_run_time()
