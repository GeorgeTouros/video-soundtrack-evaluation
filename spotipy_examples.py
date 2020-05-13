import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import spotify_creds


# login to Spotify to get the albums
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_creds['clientID'],
                                                      client_secret=spotify_creds['clientSecret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

myfriends = ['giannis_politopoulos', 'magicispells', 'george_t93', 'marioskamperis', 'anastbass']

# playlists = sp.user_playlists(myfriends[2])
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# def show_tracks(tracks):
#     for i, item in enumerate(tracks['items']):
#         track = item['track']
#         print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
#             track['name']))
#
# for name in myfriends:
#     username = name
#
#     if name:
#         playlists = sp.user_playlists(username)
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 print()
#                 print(playlist['name'])
#                 print ('  total tracks', playlist['tracks']['total'])
#                 results = sp.playlist(playlist['id'],
#                                       fields="tracks,next")
#                 tracks = results['tracks']
#                 show_tracks(tracks)
#                 while tracks['next']:
#                     tracks = sp.next(tracks)
#                     show_tracks(tracks)
#     else:
#         print("Can't get token for", username)

response = sp.featured_playlists()
print(response['message'])

while response:
    playlists = response['playlists']
    for i, item in enumerate(playlists['items']):
        print(playlists['offset'] + i, item['name'])

    if playlists['next']:
        response = sp.next(playlists)
    else:
        response = None
