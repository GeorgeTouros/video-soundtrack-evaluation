import pandas as pd
import re
from common import reg_cleaner, spotify_instance, script_start_time, script_run_time

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
    df = pd.read_csv('var\\midi_catalog.csv')
    # clean the titles up to do the query
    df = get_midi_titles(df)
    songs = get_clean_titles(df)
    songs.to_csv('var\\midi_titles.csv', index=False)
    matches = songs[songs['midi_title'].notna()]
    match_rate = 100 * len(matches) / len(songs)
    print('The match rate is %i per cent' % match_rate)
    script_run_time()
# TODO: the match rate is at 67%. Try pylast or discogs_client to see if match rate improves.

