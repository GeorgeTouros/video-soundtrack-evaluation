import re
import os
import pandas as pd
from utils.catalog_utils import *
from mysql.connector.errors import ProgrammingError
from utils.common_utils import script_start_time, script_run_time
from config.paths import audio_path, video_path, midi_path, collected_data_path
from db_handler.db_handler import DatabaseHandler
from sqlalchemy import exc

try:
    from fingerprinting import djv
except ProgrammingError:
    db = DatabaseHandler()
    db.create_db('dejavu')
    from fingerprinting import djv
from media_manipulation.video_stream import extract_audio_chunks_from_video, find_songs_in_temp_dir, \
    get_previous_and_next_values, smooth_chunk_matches, ieob_tagging_for_chunk_matches, calculate_offset_diff
from media_manipulation.video_stream import create_match_ids_per_video_segment, flag_possible_errors, get_crop_timestamps
from media_manipulation.video_manipulation import blend_audio_with_video, crop_video_to_matches

# set pandas print_options for debugging purposes
pd.options.display.width = 0

if __name__ == '__main__':
    print('Catalog creation')
    script_start_time()
    # we will remove the windows hidden files
    irrelevant_files = re.compile('(desktop\.ini)|(.*\.(jpg|db|txt|url|srt|info|nfo))')

    print("""How do you want to run the pipeline? Choose one of the modes below
    all
    midi
    audio
    video
    merge (to merge audio and video catalogs)
    prepare_fingerprints
    fingerprint (to create fingerprints)
    clip_finder (to find songs in videos)""")

    mode = input()

    if mode != 'fingerprint':
        try:
            db = DatabaseHandler('file_system_catalogs')
        except exc.OperationalError:
            db = DatabaseHandler()
            db.create_db('file_system_catalogs')
            db = DatabaseHandler('file_system_catalogs')

        db_connection = db.connection

    if mode in ["lmd", "all"]:
        lmd = get_lmd_match_names()
        dirs = []
        names = []
        for dirname, dirnames, filenames in os.walk('/media/zappatistas20/Elements/Thesis/Data/midis/lmd_matched'):
            for filename in filenames:
                dirs.append(dirname)
                names.append(filename)
        d = {'directory': dirs, 'filename': names}
        available = pd.DataFrame.from_dict(d)
        matched_keys = []
        matched_values = []
        for key in lmd.keys():
            match_key = key + '.mid'
            if match_key in available['filename'].values:
                matched_keys.append(match_key)
                name = lmd[key][0][lmd[key][0].find('/')+1:]
                matched_values.append(name)
        lmdict = {'file_lmd':matched_keys, 'match_name':matched_values}
        lookup = pd.DataFrame.from_dict(lmdict)
        joined = pd.merge(left=available, right=lookup, how='inner', left_on='filename', right_on='file_lmd')
        print(joined.head())



    if mode in ["midi", "all"]:
        # start with the midi files
        print('start midi catalog')
        # Each midi file also has an indexing file that starts with .-
        # We remove those
        irrelevant_midi = re.compile('\._|\.DS_Store')
        irrelevant_dir = ['lmd_matched', 'cariart', 'download-midi']
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
        if not db.check_for_existing_tables('video_catalog'):
            db.execute_from_file('./sql/create_video_catalog.sql')
        print('start video catalog')
        video_catalog = create_catalog(video_path, except_file=irrelevant_files)
        video_catalog = cleanup_file_titles(video_catalog, "video", allow_numbers=True)
        # video_catalog = get_clean_video_titles(video_catalog)
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
        print('write to db and dump to csv')
        merged[['pair_id', 'index_midi', 'index_audio']].to_sql('midi_audio_matches',
                                                                con=db_connection,
                                                                index=False,
                                                                if_exists='replace')
        merged.to_csv('var/midi_audio_matches.csv', index=False)

    if mode in ['clip_finder', 'all']:
        video_paths = pd.read_sql_table('video_catalog', con=db_connection)

        for video_id in video_paths[video_paths['searched'] == 0]['id'].values:
            video_path = video_paths[video_paths['id'] == video_id]['full_path'].values[0]
            file_type = video_paths[video_paths['id'] == video_id]['file_type'].values[0]
            extract_audio_chunks_from_video(video_path, 5 * 1000, file_type)
            matches = find_songs_in_temp_dir(video_id)
            match_df = pd.DataFrame.from_records(matches, columns=['chunk', 'start', 'end', 'song_id',
                                                                   'song_name', 'input_confidence', 'offset',
                                                                   'offset_seconds'])
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
            match_df = flag_possible_errors(match_df)
            if len(match_df) > 0:
                trimmer_df = get_crop_timestamps(match_df)
                trimmer_df['video_audio_match_id'] = trimmer_df['song_id'].apply(get_video_audio_match_ids, args=[int(video_id)])
                trimmer_df['video_type'] = file_type
                trimmer_df['video_id'] = video_id
                crop_video_to_matches(trimmer_df, video_path, collected_data_path + 'video/')
                trimmer_df.to_sql('audio_video_matches', con=db_connection, index=True, if_exists='append')
            db.update_value(table_name='video_catalog',
                            column_name='searched',
                            value=0,
                            where="id = {}".format(video_id))
            purge_temp_folder(get_temp_directory('video'))
            print('Completed work for ' + video_path)

    if mode in ['make_test', 'all']:

        os.chdir('./temp/test_dataset/')
        input_video = 'barry.s01e01.720p.web.h264-tbs[ettv].mkv'
        input_audio = 'M414A5061_Alice Cooper - No More Mr. Nice Guy.mp3'
        output_video = '../video/test.mp4'
        delay = 62000
        blend_audio_with_video(input_video, input_audio, output_video, delay)
        extract_audio_chunks_from_video(output_video, 5 * 1000, 'mp4')
        matches = find_songs_in_temp_dir()
        match_df = pd.DataFrame.from_records(matches, columns=['chunk', 'start', 'end', 'song_id',
                                                               'song_name', 'input_confidence', 'offset',
                                                               'offset_seconds'])
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
        match_df = flag_possible_errors(match_df)
        trimmer_df = get_crop_timestamps(match_df)
    script_run_time()
