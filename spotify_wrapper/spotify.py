import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import spotify_creds

client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds['clientID'],
                                                      client_secret=spotify_creds['clientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Spotify(object):

    def __init__(self):
        pass

    @staticmethod
    def ask_spotify(title):
        """
        for a potential title, ask spotify for a name
        :param title:
        :return: list of song attribute
        """
        song = sp.search(q=title, limit=1, type='track')
        try:
            info = song['tracks']['items'][0]
            if info:
                artist = info['artists'][0]['name']
                song_name = info['name']
                song_url = info['external_urls']['spotify']
                data = {'name': song_name, 'artist': artist, 'URL': song_url, 'clean_title': title}
            return data
        except IndexError:
            pass

    @staticmethod
    def search(**kwargs):
        results = sp.search(**kwargs)
        return results

    @staticmethod
    def playlist(*args, **kwargs):
        results = sp.playlist(*args, **kwargs)
        return results
