import os
import re
import pandas as pd
from common import reg_cleaner, script_start_time, script_run_time
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


def get_midi_titles(df):
    """
    get the titles of the midi files and return a DataFrame with them
    :param df: the midi track catalogue
    :return: df with an extra column with titles
    """
    suffix = re.compile('(.*)(\.mid|\.MID|\.Mid)')

    titles = []
    for filename in df['filename']:
        # remove suffix
        suf_search = re.search(suffix, filename)
        if suf_search:
            stripped = suf_search.group(1)
            words = reg_cleaner(stripped, numbers=False)
            titles.append(words)
        else:
            titles.append('')

    df['titles'] = titles
    df = df[df['titles'] != '']
    return df


def get_audio_titles(df):
    """
    get the titles of the mp3 files and return a DataFrame with them
    :param df: the mp3 catalogue
    :return: df with an extra column with titles
    """
    suffix = re.compile('(.*)(\.mp3|\.wav|\.MP3|\.WAV)')

    titles = []
    for filename in df['filename']:
        # remove suffix
        suf_search = re.search(suffix, filename)
        if suf_search:
            stripped = suf_search.group(1)
            words = reg_cleaner(stripped, numbers=False)
            titles.append(words)
        else:
            titles.append('')

    df['titles'] = titles
    df = df[df['titles'] != '']
    return df


def get_clean_song_titles(df):
    """
    gets the dataframe of midi titles and searches spotify to get their proper name
    :param df: the output of get_midi_titles
    :return: the original df with extra columns containing url, song name and artist
    """
    songs = []
    for title in df['titles']:
        song_info = Spotify.ask_spotify(title=title)
        if song_info:
            songs.append(song_info.copy())
        else:
            pass
    song_df = pd.DataFrame.from_records(songs)
    df = df.merge(right=song_df, left_on='titles', right_on='midi_title', how='left')
    return df


def get_film_names(df):
    # TODO: create a function that will create a catalog of the available films.
    pass


if __name__ == '__main__':
    script_start_time()
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = 'lmd_matched'
    # we also remove the windows hidden files
    irrelevant_index_file = re.compile('desktop.ini|.*\.jpg|.*\.db|.*\.txt|\.url')

    # start with the midi files
    print('start midi catalog')
    midi_dir = r'/media/zappatistas20/Elements/Thesis/Data/midis/'
    midi_catalog = create_catalog(midi_dir, irrelevant_dir, irrelevant_midi)
    print('finish midi catalog')

    # clean -up the midi title names
    print('start midi catalog cleanup')
    midi_catalog = get_midi_titles(midi_catalog)
    songs = get_clean_song_titles(midi_catalog)

    matches = songs[songs['midi_title'].notna()]
    match_rate = 100 * len(matches) / len(songs)
    print('The match rate is %i per cent' % match_rate)
    # TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

    # continue with the audio files
    print('start audio catalog')
    audio_dir = r'/media/zappatistas20/Elements/Music/'
    audio_catalog = create_catalog(audio_dir, except_file=irrelevant_index_file)
    audio_catalog = get_audio_titles(audio_catalog)
    audio_catalog = get_clean_song_titles(audio_catalog)
    audio_catalog.to_csv(r'var/audio_catalog.csv', index=False)
    print('finish audio catalog')

    # continue with the video files
    print('start video catalog')
    video_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\video'
    video_catalog = create_catalog(video_dir, except_file=irrelevant_index_file)
    video_catalog = get_film_names(video_catalog)
    video_catalog.to_csv(r'var/video_catalog.csv', index=False)
    print('finish video catalog')
    print('cleanup audio_video')

    print('dumping all to csv')

    midi_catalog.to_csv(r'var/midi_catalog.csv', index=False)
    songs.to_csv(r'var/midi_titles.csv', index=False)

    script_run_time()

