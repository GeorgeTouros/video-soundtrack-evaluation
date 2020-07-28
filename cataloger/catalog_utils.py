import os
import re

import pandas as pd

from common import reg_cleaner
from spotify_wrapper.spotify import Spotify


def create_catalog(directory, except_dir='', except_file=''):
    """
    Takes a directory as an input, and outputs a pandas DF with a full catalog of files and locations
    :param directory: the directory you want to be cataloged
    :param except_dir: optional argument to exclude irrelevant directories. Accepts str or compiled RegEx
    :param except_file: optional argument to exclude irrelevant files. Accepts str or compiled RegEx
    :return: Pandas DF with the relevant catalog
    """
    dirs = []
    names = []
    for dirname, dirnames, filenames in os.walk(directory):
        # remove unwanted directories
        if except_dir in dirnames:
            dirnames.remove(except_dir)

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
    get the titles of the midi files and return a DataFrame with them
    :param allow_numbers: boolean that passes to the regex cleaner function and allows numbers in the output.
    :param df: the midi track catalogue
    :param file_type: the type of files in the catalogue. Possible values: "audio", "video", "midi"
    :return: df with an extra column with titles
    """
    suffix = determine_irrelevant_suffices(file_type)

    titles = []
    for filename in df['filename']:
        # remove suffix
        suf_search = re.search(suffix, filename)
        if suf_search:
            stripped = suf_search.group(1)
            words = reg_cleaner(stripped, allow_numbers=allow_numbers)
            titles.append(words)
        else:
            titles.append('')

    df['title'] = titles
    df = df[df['title'] != '']
    return df


def determine_irrelevant_suffices(file_type):
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