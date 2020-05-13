import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import spotify_creds


def spotify_instance():
    # login to Spotify to get the albums
    client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds['clientID'],
                                                          client_secret=spotify_creds['clientSecret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp
