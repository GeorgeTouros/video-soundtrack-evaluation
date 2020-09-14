from pydub import AudioSegment
from pydub.playback import play
from fingerprinting.djv import ask_dejavu
from paths import temp_dir
import pandas as pd
import re
import os

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


def needs_smoothing(prev_chunk_label, next_chunk_label):
    if prev_chunk_label == next_chunk_label:
        return True
    else:
        return False


def smooth_chunk_offset(prev_offset, next_offset):
    smooth_offset = (next_offset - prev_offset) / 2
    return smooth_offset


def smooth_chunk_matches(chunk_match_data):
    chunk_label = chunk_match_data['song_id']
    chunk_offset = chunk_match_data['offset']
    prev_chunk_label = chunk_match_data['prev_song']
    prev_offset = chunk_match_data['prev_offset']
    next_chunk_label = chunk_match_data['next_song']
    next_offset = chunk_match_data['next_offset']
    if needs_smoothing(prev_chunk_label, next_chunk_label):
        return prev_chunk_label, smooth_chunk_offset(prev_offset, next_offset)
    else:
        return chunk_label, chunk_offset


# TODO: Compare the mode of the offset_seconds column for consecutive matched chunks, with the chunk_siza
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
    #os.chdir("../var/")
    #match_df = pd.DataFrame.from_records(matches, columns=['chunk', 'start', 'end', 'song_id',
    #                                                       'song_name', 'input_confidence', 'offset', 'offset_seconds'])
    match_df = pd.read_csv('../var/test_fingerprints.csv')
    match_df.sort_values(by='start', inplace=True)
    match_df['prev_song'] = match_df['song_id'].shift(1)
    match_df['prev_offset'] = match_df['offset'].shift(1)
    match_df['next_song'] = match_df['song_id'].shift(-1)
    match_df['next_offset'] = match_df['offset'].shift(-1)

    match_df['smooth_song_id'], match_df['smooth_song_label'] = zip(*match_df.apply(func=smooth_chunk_matches, axis=1))

    match_df.to_csv('test_fingerprints.csv', index=False)
    print('Done')
    # res = ask_dejavu(temp_dir+'vid_chunk__2730000__2760000.mp3')
    # res = ask_dejavu('/home/zappatistas20/PycharmProjects/thesis_dataset_creation/temp/M25067A142098_11  NANCY SINATRA - THESE BOOTS ARE MADE FOR WALKING.mp3')
    #print(res['results'])
