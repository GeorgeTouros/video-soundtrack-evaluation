from config.settings import CHUNK_SIZE_MS, SAMPLE_RATE, CHANNELS, AUDIO_FILE_TYPE
from media_manipulation import audio_conversions
from fingerprinting.djv import ask_dejavu
from media_manipulation.video_manipulation import crop_video_to_matches
from utils.catalog_utils import get_temp_directory
import pandas as pd
import re
import os
from time import time
from statistics import mode
from statistics import StatisticsError


def extract_audio_chunks_from_video(video_file, chunk_size=CHUNK_SIZE_MS, file_type="mp4", temp_dir=None):
    if not temp_dir:
        temp_dir = get_temp_directory('video')
    print('Loading file')
    temp_file_name = temp_dir + 'full_film.' + AUDIO_FILE_TYPE
    audio = audio_conversions.load_and_convert_with_ffmpeg(video_file,
                                                           temp_file_name,
                                                           sample_rate=SAMPLE_RATE,
                                                           channels=CHANNELS,
                                                           file_type=AUDIO_FILE_TYPE)
    # ffmpeg_extract_audio(video_file, temp_file_name, bitrate=16000, fps=8000)
    # print('Converting to suitable format')
    # audio = audio_conversions.load_and_convert_stereo_to_mono_8k(temp_file_name, format='mp3')
    print('chunking')
    chunk_index = 0
    for chunk in audio[::chunk_size]:
        file_name = 'vid_chunk__' + str(chunk_index) + '__' + str(chunk_index + chunk_size) + '.' + AUDIO_FILE_TYPE
        try:
            print('exporting chunk ' + file_name)
            chunk.export(temp_dir + file_name, AUDIO_FILE_TYPE)
        except FileNotFoundError:
            oldmask = os.umask(000)
            os.makedirs(temp_dir, exist_ok=True, mode=0o755)
            os.umask(oldmask)
            chunk.export(temp_dir + file_name, AUDIO_FILE_TYPE)
        chunk_index += chunk_size
    os.unlink(temp_file_name)


def parse_recognition_results(dejavu_results):
    song_id = dejavu_results['song_id']
    song_name = str(dejavu_results['song_name'], 'utf-8')
    input_confidence = dejavu_results['input_confidence']
    offset = dejavu_results['offset']
    offset_seconds = dejavu_results['offset_seconds']
    return song_id, song_name, input_confidence, offset, offset_seconds


def parse_timestamps_from_chunk_name(chunk_name):
    pattern = re.compile('vid_chunk__(\d*)__(\d*)\..{3}')
    re_match = re.search(pattern, chunk_name)
    start = re_match[1]
    end = re_match[2]
    return start, end


def find_songs_in_temp_dir(video_id, temp_dir):
    songs = []
    timediffs = []
    ind = 1
    for chunk in sorted(os.listdir(temp_dir)):
        time1 = time()
        if "chunk" in str(chunk):
            result = ask_dejavu(temp_dir + chunk)
            print("Percentage completed: {}".format(round(ind / len(os.listdir(temp_dir)), 3)))
            start, end = parse_timestamps_from_chunk_name(chunk)
            try:
                if result['results'][0]['input_confidence'] < 0.01:
                    songs.append((chunk, start, end, None, None, None, None, None))
                    # print('Nothing')
                else:
                    match = result['results'][0]
                    # print(match)
                    song_id, song_name, input_confidence, offset, offset_seconds = parse_recognition_results(match)
                    songs.append((chunk, start, end, song_id, song_name, input_confidence, offset, offset_seconds))
            except IndexError:
                songs.append((chunk, start, end, None, None, None, None, None))
                # print('Nothing')
            ind += 1
            time2 = time()
            timediff = time2 - time1
            timediffs.append(timediff)
        else:
            continue
    with open("./var/timediffs_{}.txt".format(video_id), "w") as outfile:
        outfile.write("\n".join(str(item) for item in timediffs))
    return songs


def get_previous_and_next_values(df, columns_of_interest):
    for column in columns_of_interest:
        if column in df.columns:
            new_column_prev_name = 'prev_' + column
            df[new_column_prev_name] = df[column].shift(1)
            new_column_next_name = 'next_' + column
            df[new_column_next_name] = df[column].shift(-1)
    return df


def needs_smoothing(prev_chunk_label, next_chunk_label, chunk_label):
    if prev_chunk_label == next_chunk_label and prev_chunk_label != chunk_label:
        return True
    else:
        return False


def smooth_chunk_offset(prev_offset, next_offset):
    smooth_offset = (next_offset - prev_offset) / 2
    return smooth_offset


def smooth_chunk_matches(chunk_match_data):
    """
    for each row, if the previous match is the same as the next one, change the label of the row and set the offset as
    the mean between the 2 rows.
    :param chunk_match_data:
    :return: smooth song label, smooth song offset
    """
    chunk_label = chunk_match_data['song_id']
    chunk_offset = chunk_match_data['offset_seconds']
    prev_chunk_label = chunk_match_data['prev_song_id']
    prev_offset = chunk_match_data['prev_offset_seconds']
    next_chunk_label = chunk_match_data['next_song_id']
    next_offset = chunk_match_data['next_offset_seconds']
    if needs_smoothing(prev_chunk_label, next_chunk_label, chunk_label):
        return prev_chunk_label, smooth_chunk_offset(prev_offset, next_offset)
    else:
        return chunk_label, chunk_offset


def ieob_tagging_for_chunk_matches(chunk_match_data):
    prev_chunk_label = chunk_match_data['prev_song_id']
    chunk_label = chunk_match_data['song_id']
    next_chunk_label = chunk_match_data['next_song_id']
    if prev_chunk_label != chunk_label and chunk_label == next_chunk_label:
        return "B"
    if prev_chunk_label == chunk_label and chunk_label == next_chunk_label:
        return "I"
    if prev_chunk_label == chunk_label and chunk_label != next_chunk_label:
        return "E"
    else:
        return "O"


def calculate_offset_diff(chunk_match_data):
    chunk_offset = chunk_match_data['offset_seconds']
    prev_offset = chunk_match_data['prev_offset_seconds']
    tag = chunk_match_data['match_tag']
    if tag in ['I', 'E']:
        offset_diff = round(chunk_offset - prev_offset, 0)
        return offset_diff
    else:
        return None


def create_match_ids_per_video_segment(tags):
    match_id = 0
    match_ids = []
    for tag in tags:
        if tag == 'B':
            match_id += 1
            match_ids.append(match_id)
        elif tag in ['I', 'E']:
            match_ids.append(match_id)
        else:
            match_ids.append(None)
    return match_ids


def get_match_area_mode(match_area):
    try:
        return mode(match_area)
    except StatisticsError:
        return None


def flag_possible_errors(df):
    filter_df = df.loc[df['match_id'].notna()].copy()
    grouped_df = filter_df.groupby('match_id')['offset_diff']
    modes = grouped_df.apply(get_match_area_mode)
    valid_modes = modes[modes.notna()].index.values
    sizes = grouped_df.size()
    tp = sizes[sizes >= 3].index.values
    filter_df['too_small'] = [0 if i in tp else 1 for i in filter_df['match_id'].values]
    filter_df['invalid_mode'] = [0 if i in valid_modes else 1
                                 for i in filter_df['match_id'].values]
    return filter_df


def get_crop_timestamps(df):
    tims = df.groupby(by=['match_id', 'song_id']).agg({'start': "min",
                                                       "end": "max",
                                                       "invalid_mode": "max"})
    tims.reset_index(inplace=True)
    return tims
