import os
import re
from shutil import copyfile
import pandas as pd
from config.paths import collected_data_path, local_temp_dir
from spotify_wrapper.spotify import Spotify
from math import ceil


def create_catalog(directory, except_dir=[], except_file=''):
    """
    Takes a directory as an input, and outputs a pandas DF with a full catalog of files and locations
    :param directory: the directory you want to be cataloged
    :param except_dir: optional argument to exclude irrelevant directories. Accepts list
    :param except_file: optional argument to exclude irrelevant files. Accepts str or compiled RegEx
    :return: Pandas DF with the relevant catalog
    """
    dirs = []
    names = []
    for dirname, dirnames, filenames in os.walk(directory):
        # remove unwanted directories
        for bad_dir in except_dir:
            if bad_dir in dirnames:
                dirnames.remove(bad_dir)
        for filename in filenames:
            if re.search(except_file, str(filename)):
                filenames.remove(filename)
            else:
                dirs.append(dirname)
                names.append(filename)
    d = {'directory': dirs, 'filename': names}

    output = pd.DataFrame.from_dict(d)
    return output


def cleanup_file_titles(df, file_type, allow_numbers=False):
    """
    get the titles of a file and return a DataFrame with a title column and a filetype column
    :param allow_numbers: boolean that passes to the regex cleaner function and allows numbers in the output.
    :param df: the midi track catalogue
    :param file_type: the type of files in the catalogue. Possible values: "audio", "video", "midi"
    :return: df with an extra column with titles and file type
    """
    suffix = determine_relevant_suffices(file_type)

    titles = []
    file_types = []
    for filename in df['filename']:
        # only keep relevant file types
        suf_search = re.search(suffix, filename)
        if suf_search:
            # strip from suffix
            stripped = suf_search.group(1)
            words = reg_cleaner(stripped, allow_numbers=allow_numbers)
            titles.append(words)
            suf = suf_search.group(2).strip(".")
            file_types.append(suf)
        else:
            titles.append('')
            file_types.append('')

    df['title'] = titles
    df['file_type'] = file_types
    df = df[df['title'] != '']
    return df


def determine_relevant_suffices(file_type):
    if file_type == "midi":
        suffix = re.compile('(.*)(\.mid|\.MID|\.Mid)')
    elif file_type == "audio":
        suffix = re.compile('(.*)(\.mp3|\.wav|\.MP3|\.WAV)')
    elif file_type == "video":
        suffix = re.compile('(.*)(\.mp4|\.mkv|\.avi)')
    else:
        raise ValueError
    return suffix


def get_clean_song_titles_from_spotify(df):
    """
    gets the dataframe of song titles and searches spotify to get their proper name
    :param df: the output of get_titles
    :return: the original df with extra columns containing url, song name and artist
    """
    songs = []
    for title in df['title']:
        song_info = Spotify.ask_spotify(title=title)
        if song_info:
            songs.append(song_info.copy())
        else:
            pass
    song_df = pd.DataFrame.from_records(songs)
    df = df.merge(right=song_df, left_on='title', right_on='clean_title', how='left')
    df.drop(columns='clean_title', inplace=True)
    df.rename(columns={'name': 'spotify_name', 'artist': 'spotify_artist', 'URL': 'spotify_URL'}, inplace=True)
    return df


FILENAME_STOPWORDS = ['bdrip', 'brrip', '1080p', '720p', 'aac',
                      'www', 'yifi', 'yts', 'anoxmous', 'bluray', 'hdtv', 'org', 'rcg', 'jh', 'rg2',
                      'webrip', 'criterion', 'dvdrip', 'x264', 'xvid', 'gaz', 'bz2', 'da', 'dc', 'dwb', 'jc2',
                      'dm', 'kar', 'karaoke', 'version', 'jpp', 'jk', 'mc', 'rt', 'gw', 'gc9', 'bb', 'gp', 'gl',
                      'mix', 'remix', 'dj', 'nr', 'song', 'k', 'gr', 'cm', 'v1', 'mw', 'rw', 'bz3', 'v2', 'fs',
                      'yify', 'ehhhh', 'blu', 'ray', 'vppv', 'rip', 'enc', 'amzn'
                      ]


def reg_cleaner(string, allow_numbers=True):
    """
    simple function to convert string to lowercase and remove special characters
    :param allow_numbers: specify if you want to allow numbers or not (default yes)
    :param string: the string you want to clean
    :return: the clean string
    """
    if allow_numbers:
        remove_special = re.sub('[^A-Za-z0-9]+', ' ', string)
    else:
        remove_special = re.sub('[^A-Za-z]+', ' ', string)

    pascalcase = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', remove_special)

    clean_string = pascalcase.lower()

    removed_stopwords = remove_stopwords(clean_string)

    removed_multi_space = remove_multi_spaces(removed_stopwords)

    return removed_multi_space


def remove_stopwords(string):
    removed_stopwords = ' '.join([word for word in string.split() if word not in FILENAME_STOPWORDS])
    return removed_stopwords


def remove_multi_spaces(string):
    multiple_spaces = re.compile('(\s\s+)')
    stripped_string = re.sub(multiple_spaces, ' ', string)
    return stripped_string


def get_audio_midi_match_ids(midi_id, audio_id):
    index = 'M' + str(midi_id) + 'A' + str(audio_id)
    return index


def get_video_audio_match_ids(audio_id, video_id):
    index = "V" + str(int(video_id)) + "A" + str(int(audio_id))
    return index


def setup_collection_directory(new_dir=collected_data_path):
    new_midi_dir = new_dir + 'midi/'
    new_audio_dir = new_dir + 'audio/'
    new_video_dir = new_dir + 'video/'
    oldmask = os.umask(000)
    os.makedirs(new_midi_dir, exist_ok=True, mode=0o755)
    os.makedirs(new_audio_dir, exist_ok=True, mode=0o755)
    os.makedirs(new_video_dir, exist_ok=True, mode=0o755)
    os.umask(oldmask)
    return new_midi_dir, new_audio_dir, new_video_dir


def get_collection_directory(data_type):
    """
    retrieve the collection directory for the specific data type
    :param data_type: either one of audio, video or midi
    :return: the directory
    """
    if data_type in ['audio', 'midi', 'video']:
        dir = collected_data_path + str(data_type) + '//'
        return dir
    else:
        raise ValueError('not acceptable data type')


def setup_curated_video_dir():
    vid_dir = get_collection_directory('video')
    new_video_dir = vid_dir + '/curated/'
    oldmask = os.umask(000)
    os.makedirs(new_video_dir, exist_ok=True, mode=0o755)
    os.umask(oldmask)
    return new_video_dir


def collect_matched_files(row, new_midi_path, new_audio_path):
    midi_path = row['directory_midi']
    midi_file_name = row['filename_midi']
    midi_index = row['index_midi']
    audio_index = row['index_audio']
    audio_path = row['directory_audio']
    audio_file_name = row['filename_audio']
    pair_id = get_audio_midi_match_ids(midi_index, audio_index)

    new_midi_name = get_new_file_name(midi_file_name, pair_id)
    complete_source_file_path = midi_path + '/' + midi_file_name
    complete_destination_file_path = new_midi_path + '/' + new_midi_name
    copyfile(complete_source_file_path, complete_destination_file_path)
    print('file ' + complete_source_file_path + ' copied sucessfully as ' + complete_destination_file_path)

    new_audio_name = get_new_file_name(audio_file_name, pair_id)
    complete_source_file_path = audio_path + '/' + audio_file_name
    complete_destination_file_path = new_audio_path + '/' + new_audio_name
    copyfile(complete_source_file_path, complete_destination_file_path)
    print('file ' + complete_source_file_path + ' copied sucessfully as ' + complete_destination_file_path)

    return pair_id


def get_new_file_name(old_file_name, pair_id):
    new_name = str(pair_id) + '_' + str(old_file_name)
    return new_name


def check_if_all_files_in_temp_dir(original_file_dir, temp_file_dir):
    old_files = os.listdir(original_file_dir)
    temp_files = os.listdir(temp_file_dir)
    return set(old_files) == set(temp_files)


def get_temp_directory(data_type):
    """
    retrieve the collection directory for the specific data type
    :param data_type: either one of audio, video or midi
    :return: the directory
    """
    if data_type in ['audio', 'midi', 'video']:
        dir = local_temp_dir + str(data_type) + '/'
        return dir
    else:
        raise ValueError('not acceptable data type')


def setup_batch_temp_folders(batch_size, input_folder, temp_dir):
    total_files = len(os.listdir(input_folder))
    folders_needed = ceil(total_files/batch_size)
    folder_names = []
    for i in range(0, folders_needed):
        new_temp_dir_name = temp_dir+"audio_{}/".format(i)
        oldmask = os.umask(000)
        os.makedirs(new_temp_dir_name, exist_ok=True, mode=0o755)
        os.umask(oldmask)
        folder_names.append(new_temp_dir_name)
    return folder_names


def purge_temp_folder(temp_folder):
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)