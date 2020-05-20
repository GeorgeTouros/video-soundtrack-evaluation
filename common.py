import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import spotify_creds
import re
from datetime import datetime


def spotify_instance():
    # login to Spotify to get the albums
    client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds['clientID'],
                                                          client_secret=spotify_creds['clientSecret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def ask_spotify(title, sp):
    """
    for a potential title, ask spotify for a name
    :param title:
    :param sp: a spotify instance
    :return: list of song attribute
    """
    song = sp.search(q=title, limit=1, type='track')
    try:
        info = song['tracks']['items'][0]
        if info:
            artist = info['artists'][0]['name']
            song_name = info['name']
            song_url = info['external_urls']['spotify']
            data = {'name': song_name, 'artist': artist, 'URL': song_url, 'midi_title': title}
        return data
    except IndexError:
        pass


def reg_cleaner(string, numbers=True):
    """
    simple function to convert string to lowercase and remove special characters
    :param numbers: specify if you want to allow numbers or not (default yes)
    :param string: the string you want to clean
    :return: the clean string
    """
    if numbers:
        clean_string = re.sub('[^A-Za-z0-9]+', ' ', string).lower()
    else:
        clean_string = re.sub('[^A-Za-z]+', ' ', string).lower()
    return clean_string

def script_start_time():
    start_time = datetime.now()
    print('Script started running at: '+str(start_time))


def script_run_time():
    end_time = datetime.now()
    print('Script ended at:'+str(end_time))