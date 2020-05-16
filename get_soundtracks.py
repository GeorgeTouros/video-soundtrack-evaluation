from common import spotify_instance
import pandas as pd
import re
import pprint

# load spotify instance
sp = spotify_instance()

# list of movies with rock songs
films = ['Forrest Gump', 'Almost Famous',
         'Blues Brothers', 'School of Rock',
         'Grease', 'Dazed and Confused',
         'Waynes World', 'High Fidelity',
         'Purple Rain']


def reg_cleaner(string):
    """
    simple function to convert string to lowercase and remove special characters
    :param string: the string you want to clean
    :return: the clean string
    """
    clean_string = re.sub('[^A-Za-z0-9]+', ' ', string).lower()
    return clean_string


def get_film_albums(film_list=films):
    albums = pd.DataFrame()
    for film in film_list:
        result = sp.search(q=film, limit=50, type='album')
        df = pd.DataFrame.from_dict(result['albums']['items'])
        df.head()
        albums = albums.append(df)
    return albums


def get_film_playlists(film_list=films):
    playlists = pd.DataFrame()
    for film in film_list:
        result = sp.search(q=film, limit=50, type='playlist')
        df = pd.DataFrame.from_dict(result['playlists']['items'])
        df.head()
        playlists = playlists.append(df)
    return playlists


def find_film_soundtrack_album(albums):
    albums = albums.loc[albums['total_tracks'] > 1]
    return albums


def find_film_soundtrack_playlist(playlists, film_list=films):
    playlists['clean_names'] = [reg_cleaner(name) for name in playlists['name']]
    playlists['spotify_url'] = [str(url).strip('{\'spotify\': \'').strip("\'}") for url in playlists['external_urls']]
    clean_films = [reg_cleaner(film) for film in film_list]
    clean_playlists = pd.DataFrame()
    for film in clean_films:
        pattern = re.compile('.*('+str(film)+').*(soundtrack|film)')
        playlists['has_film'] = [film if re.search(pattern, name) else None for name in playlists['clean_names']]
        row = playlists[playlists['has_film'].notna()].head(1)
        clean_playlists = clean_playlists.append(row)
    return clean_playlists


def find_songs_in_playlist(playlists):
    useful = playlists[['id', 'has_film']]
    rows = pd.DataFrame()
    for playlist, film in useful.values:
        results = sp.playlist(playlist, fields="tracks,next")
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            track = item['track']
            artist = track['artists'][0]['name']
            track_name = track['name']
            url = track['external_urls']['spotify']
            data = {'film': film,
                    'track_name': track_name,
                    'artist': artist,
                    'url': url}
            rows = rows.append(data, ignore_index=True)
    rows = rows[['film', 'track_name', 'artist', 'url']]
    return rows


if __name__ == '__main__':
    albums = get_film_albums()
    albums = find_film_soundtrack_album(albums)
    albums.to_csv('var\\soundtracks.csv', index=False)
    playlists = get_film_playlists()
    playlists = find_film_soundtrack_playlist(playlists)
    playlists.to_csv('var\\film_playlists.csv', index=False)
    tracks = find_songs_in_playlist(playlists)
    tracks.to_csv('var\\tracks.csv',index=False)

# TODO: match with midi file names
