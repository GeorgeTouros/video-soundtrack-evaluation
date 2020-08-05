import re
import pandas as pd
from cataloger.catalog_utils import create_catalog, cleanup_file_titles, get_match_ids, setup_collection_directory
from cataloger.catalog_utils import get_clean_song_titles_from_spotify, collect_matched_files
from common import script_start_time, script_run_time
from paths import audio_path, video_path, midi_path
from db_handler.db_handler import DatabaseHandler
from sqlalchemy import exc

# set pandas print_options for debugging purposes
pd.options.display.width = 0

if __name__ == '__main__':
    print('Catalog creation')
    script_start_time()
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = ['lmd_matched', 'cariart', 'download-midi']
    # we also remove the windows hidden files
    irrelevant_files = re.compile('(desktop\.ini)|(.*\.(jpg|db|txt|url|srt|info|nfo))')

    try:
        db = DatabaseHandler('file_system_catalogs')
    except exc.OperationalError:
        db = DatabaseHandler()
        db.create_db('file_system_catalogs')
        db = DatabaseHandler('file_system_catalogs')

    db_connection = db.connection

    print("""How do you want to run the pipeline? Choose one of the modes below
    all
    midi
    audio
    video
    merge (to merge audio and video catalogs)
    fingerprint (to create fingerprints)
    clip_finder (to find songs in videos)""")

    mode = input()

    if mode in ["midi", "all"]:
        # start with the midi files
        print('start midi catalog')
        midi_catalog = create_catalog(midi_path, irrelevant_dir, irrelevant_midi)
        print('finish initial midi catalog')

        # clean -up the midi title names
        print('start midi catalog cleanup')
        midi_catalog = cleanup_file_titles(midi_catalog, "midi", allow_numbers=True)
        midi_catalog = get_clean_song_titles_from_spotify(midi_catalog)
        midi_catalog.drop_duplicates(inplace=True)
        midi_catalog.to_csv(r'var/midi_catalog.csv', index=False)
        midi_catalog.to_sql('midi_catalog', con=db_connection, if_exists='replace')

        matches = midi_catalog[midi_catalog['spotify_name'].notna()]
        recall = 100 * len(matches) / len(midi_catalog)
        print('The recall is %i per cent' % recall)
        # TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

    if mode in ["audio", "all"]:
        # continue with the audio files
        print('start audio catalog')
        audio_catalog = create_catalog(audio_path, except_file=irrelevant_files, except_dir=['Bootlegs'])
        audio_catalog = cleanup_file_titles(audio_catalog, "audio")
        audio_catalog = get_clean_song_titles_from_spotify(audio_catalog)
        audio_catalog.drop_duplicates(inplace=True)
        audio_catalog.to_csv(r'var/audio_catalog.csv', index=False)
        audio_catalog.to_sql('audio_catalog', con=db_connection, if_exists='replace')
        print('finish audio catalog')

    if mode in ['video', 'all']:
        # continue with the video files
        print('start video catalog')
        video_catalog = create_catalog(video_path, except_file=irrelevant_files)
        video_catalog = cleanup_file_titles(video_catalog, "video", allow_numbers=True)
        # video_catalog = get_clean_video_titles(video_catalog)
        video_catalog.to_csv(r'var/video_catalog.csv', index=False)
        video_catalog.to_sql('video_catalog', con=db_connection, if_exists='replace')
        print('finish video catalog')

    if mode in ['merge', 'all']:
        print('Loading tables')
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
        merged['pair_id'] = merged.apply(collect_matched_files, new_midi_path=new_midi_dir, new_audio_path=new_audio_dir, axis=1)
        print('write to db and dump to csv')
        merged[['pair_id', 'index_midi', 'index_audio']].to_sql('midi_audio_matches',
                                                                con=db_connection,
                                                                index=False,
                                                                if_exists='replace')
        merged.to_csv('var/midi_audio_matches.csv', index=False)

    if mode in ['fingerprint', 'all']:
        print('still work in progress')

    script_run_time()
