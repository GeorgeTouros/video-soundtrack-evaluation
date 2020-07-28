import os
import re
import pandas as pd
from common import reg_cleaner, script_start_time, script_run_time
from spotify_wrapper.spotify import Spotify
from paths import audio_path, video_path, midi_path
import db_handler

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


def get_titles(df, type, allow_numbers=False):
    """
    get the titles of the midi files and return a DataFrame with them
    :param allow_numbers: boolean that passes to the regex cleaner function and allows numbers in the output.
    :param df: the midi track catalogue
    :param type: the type of files in the catalogue. Possible values: "audio", "video", "midi"
    :return: df with an extra column with titles
    """
    if type == "midi":
        suffix = re.compile('(.*)(\.mid|\.MID|\.Mid)')
    elif type == "audio":
        suffix = re.compile('(.*)(\.mp3|\.wav|\.MP3|\.WAV)')
    elif type == "video":
        suffix = re.compile('(.*)(\.mp4|\.mkv|\.avi)')
    else:
        raise ValueError

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

    df['titles'] = titles
    df = df[df['titles'] != '']
    return df


def get_clean_song_titles(df):
    """
    gets the dataframe of song titles and searches spotify to get their proper name
    :param df: the output of get_titles
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
    df = df.merge(right=song_df, left_on='titles', right_on='clean_title', how='left')
    return df


def get_clean_video_titles(df):
    """
    gets the dataframe of video titles and cleans it up from irrelevant words and then
    searches IMDb to get their proper name
    :param df: the output of get_titles
    :return: the original df with extra columns containing url, song name and artist
    """


    cleaner_titles = []

    return df


if __name__ == '__main__':
    print('Catalog creation')
    script_start_time()
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = 'lmd_matched'
    # we also remove the windows hidden files
    irrelevant_files = re.compile('(desktop\.ini)|(.*\.(jpg|db|txt|url|srt|info|nfo))')

    engine = db_handler.engine

    db_handler.create_db('file_system_catalogs')

    mode = input('How do you want to run the whole pipeline? (all, midi, audio, video)')

    if mode in ["midi", "all"] :
        # start with the midi files
        print('start midi catalog')
        midi_dir = midi_path
        midi_catalog = create_catalog(midi_dir, irrelevant_dir, irrelevant_midi)
        print('finish initial midi catalog')

        # clean -up the midi title names
        print('start midi catalog cleanup')
        midi_catalog = get_titles(midi_catalog, "midi", allow_numbers=True)
        songs = get_clean_song_titles(midi_catalog)
        songs.to_csv(r'var/midi_catalog.csv', index=False)
        songs.to_sql('file_system_catalogs.dbo.midi_catalog', con=engine, if_exists='replace')

        matches = songs[songs['clean_title'].notna()]
        recall = 100 * len(matches) / len(songs)
        print('The recall is %i per cent' % recall)
        # TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

    if mode in ["audio", "all"]:
        # continue with the audio files
        print('start audio catalog')
        audio_dir = audio_path
        audio_catalog = create_catalog(audio_dir, except_file=irrelevant_files)
        audio_catalog = get_titles(audio_catalog, "audio")
        audio_catalog = get_clean_song_titles(audio_catalog)
        audio_catalog.to_csv(r'var/audio_catalog.csv', index=False)
        audio_catalog.to_sql('audio_catalog', con=engine, if_exists='replace')
        print('finish audio catalog')

    if mode in ['video', 'all']:
        # continue with the video files
        print('start video catalog')
        video_dir = video_path
        video_catalog = create_catalog(video_dir, except_file=irrelevant_files)
        video_catalog = get_titles(video_catalog, "video", allow_numbers=True)
        # video_catalog = get_clean_video_titles(video_catalog)
        video_catalog.to_csv(r'var/video_catalog.csv', index=False)
        video_catalog.to_sql('video_catalog', con=engine, if_exists='replace')
        print('finish video catalog')

    script_run_time()

