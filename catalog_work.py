import os
import re
import pandas as pd
from common import reg_cleaner, spotify_instance, script_start_time, script_run_time


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


def identify_ennio_names(cat):
    """
    adds an extra column to the catalog df with the clean title and the id.
    :param cat: the catalog dataframe
    :return: the clean df
    """
    patterns = re.compile('title_(.*)-id_(.*?)(-.*|$)')
    titles = []
    ids = []
    for filename in cat['filename']:
        search = re.search(patterns, str(filename))
        if search:
            title = search.group(1)
            db_id = search.group(2)
            titles.append(title)
            ids.append(db_id)
        else:
            titles.append(' ')
            ids.append(' ')
    cat['title'] = titles
    cat['id'] = ids
    return cat

def merge_ennio_audio_video_catalogs(audio_df, video_df):
    """
    takes the ennio catalogues and only keeps the files that exist in both
    :param audio_df: a pandas dataframe
    :param video_df: another pandas dataframe
    :return: joined dataframe
    """
    audio_df.set_index(keys='title', inplace=True)
    video_df.set_index(keys='title', inplace=True)

    merged = audio_df.merge(right=video_df,
                            left_index=True,
                            right_index=True,
                            how='inner',
                            suffixes=('_audio', '_video'))
    merged.reset_index(inplace=True)
    return merged


sp = spotify_instance()

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


def ask_spotify(title):
    """
    for a potential title, ask spotify for a name
    :param title:
    :return: list of song attribute
    """
    song = sp.search(q=title, limit=1, type='track')
    try:
        info = song['tracks']['items'][0]
        return info
    except IndexError:
        pass


def get_clean_titles(df):
    """
    gets the dataframe of midi titles and searches spotify to get their proper name
    :param df: the output of get_midi_titles
    :return: the original df with extra columns containing url, song name and artist
    """
    songs = []
    for title in df['titles']:
        song_info = ask_spotify(title)
        if song_info:
            artist = song_info['artists'][0]['name']
            song_name = song_info['name']
            song_url = song_info['external_urls']['spotify']
            data = {'name': song_name, 'artist': artist, 'URL': song_url, 'midi_title': title}
            songs.append(data.copy())
        else:
            pass
    song_df = pd.DataFrame.from_records(songs)
    df = df.merge(right=song_df, left_on='titles', right_on='midi_title', how='left')
    return df


if __name__ == '__main__':
    script_start_time()
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = 'lmd_matched'
    # we also remove the windows hidden files
    irrelevant_index_file = re.compile('desktop.ini')

    # start with the midi files
    print('start midi catalog')
    midi_dir = 'data\\midis\\'
    midi_catalog = create_catalog(midi_dir, irrelevant_dir, irrelevant_midi)
    print('finish midi catalog')

    # clean -up the midi title names
    print('start midi catalog cleanup')
    midi_catalog = get_midi_titles(midi_catalog)
    songs = get_clean_titles(midi_catalog)

    matches = songs[songs['midi_title'].notna()]
    match_rate = 100 * len(matches) / len(songs)
    print('The match rate is %i per cent' % match_rate)
    # TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

    # continue with the audio files
    print('start audio catalog')
    audio_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\audio'
    audio_catalog = create_catalog(audio_dir, except_file=irrelevant_index_file)
    audio_catalog = identify_ennio_names(audio_catalog)
    audio_catalog.to_csv('var\\audio_catalog.csv', index=False)
    print('finish audio catalog')

    # continue with the video files
    print('start video catalog')
    video_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\video'
    video_catalog = create_catalog(video_dir, except_file=irrelevant_index_file)
    video_catalog = identify_ennio_names(video_catalog)
    video_catalog.to_csv('var\\video_catalog.csv', index=False)
    print('finish video catalog')
    print('cleanup audio_video')
    merge = merge_ennio_audio_video_catalogs(audio_catalog, video_catalog)

    print('dumping all to csv')

    merge.to_csv('var\\ennio_catalog.csv', index=False)
    midi_catalog.to_csv('var\\midi_catalog.csv', index=False)
    songs.to_csv('var\\midi_titles.csv', index=False)

    script_run_time()

