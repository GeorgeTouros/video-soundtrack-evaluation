from pydub import AudioSegment
from pydub.playback import play
from fingerprinting.djv import ask_dejavu
from paths import temp_dir
import pandas as pd
import re
import os
from statistics import mode
from statistics import StatisticsError

CHUNK_SIZE = 30 * 1000  # ms


def extract_audio_chunks_from_video(video_file, chunk_size=CHUNK_SIZE):
    print('Loading file')
    audio = AudioSegment.from_file(video_file, "mp4")
    audio = audio.set_frame_rate(44100)
    # TODO: Add multiple file extension functionality
    chunk_index = 0
    for chunk in audio[::chunk_size]:
        file_name = 'vid_chunk__' + str(chunk_index) + '__' + str(chunk_index + chunk_size) + '.mp3'
        try:
            print('exporting chunk ' + file_name)
            chunk.export(temp_dir + file_name, "mp3")
        except FileNotFoundError:
            oldmask = os.umask(000)
            os.makedirs(temp_dir, exist_ok=True, mode=0o755)
            os.umask(oldmask)
            chunk.export(temp_dir + file_name, "mp3")
        chunk_index += chunk_size


def parse_recognition_results(dejavu_results):
    song_id = dejavu_results['song_id']
    song_name = str(dejavu_results['song_name'], 'utf-8')
    input_confidence = dejavu_results['input_confidence']
    offset = dejavu_results['offset']
    offset_seconds = dejavu_results['offset_seconds']
    return song_id, song_name, input_confidence, offset, offset_seconds


def parse_timestamps_from_chunk_name(chunk_name):
    pattern = re.compile('vid_chunk__(\d*)__(\d*)\.mp3')
    re_match = re.search(pattern, chunk_name)
    start = re_match[1]
    end = re_match[2]
    return start, end


def find_songs_in_temp_dir():
    songs = []
    for chunk in os.listdir(temp_dir):
        result = ask_dejavu(temp_dir+chunk)
        print(chunk)
        try:
            if result['results'][0]['input_confidence'] < 0.2:
                print('Nothing')
            else:
                match = result['results'][0]
                print(match)
                song_id, song_name, input_confidence, offset, offset_seconds = parse_recognition_results(match)
                start, end = parse_timestamps_from_chunk_name(chunk)
                songs.append((chunk, start, end, song_id, song_name, input_confidence, offset, offset_seconds))
        except IndexError:
            print('Nothing')
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


def create_match_ids(tags):
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


def get_true_positives(df):
    filter_df = df[df['match_ids'].notna()]
    grouped_df = filter_df.groupby('match_ids')['offset_diff']
    modes = grouped_df.apply(get_match_area_mode)
    tp = modes[modes.notna()].index.values
    tp_df = df[df['match_ids'].isin(tp)]
    return tp_df


# TODO: Combine the matched chunks into one and crop the video in the appropriate timestamps

# these boots are made for walking should be on minute 45 of this film
#film_audio = AudioSegment.from_file(
#    r"/home/zappatistas20/Videos/Full Metal Jacket (1987)/Full.Metal.Jacket.1987.720p.BrRip.YIFY.mp4",
#    "mp4")

#ask_dejavu(chunk)


# save = mp4_version.export(r"/home/zappatistas20/Videos/Full Metal Jacket (1987)/AUDIOFull.Metal.Jacket.1987.720p.BrRip.YIFY.mp3",
#                          format="mp3")


if __name__ == '__main__':
    #test_file_path = r"/home/zappatistas20/Videos/Full Metal Jacket (1987)/Full.Metal.Jacket.1987.720p.BrRip.YIFY.mp4"
    #extract_audio_chunks_from_video(test_file_path, 5*1000)
    #matches = find_songs_in_temp_dir()
    #match_df = pd.DataFrame.from_records(matches, columns=['chunk', 'start', 'end', 'song_id',
    #                                                       'song_name', 'input_confidence', 'offset', 'offset_seconds'])
    #match_df.sort_values(by='start', inplace=True)
    #match_df.to_csv('../var/test_fingerprints.csv', index=False)
    match_df = pd.read_csv('../var/test_fingerprints.csv')
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
    match_df['match_ids'] = create_match_ids(match_df['match_tag'].values)
    match_df = get_true_positives(match_df)
    match_df.to_csv('../var/test_smoothing.csv', index=False)
    print('Done')
    # res = ask_dejavu(temp_dir+'vid_chunk__2730000__2760000.mp3')
    # res = ask_dejavu('/home/zappatistas20/PycharmProjects/thesis_dataset_creation/temp/M25067A142098_11  NANCY SINATRA - THESE BOOTS ARE MADE FOR WALKING.mp3')
    #print(res['results'])
