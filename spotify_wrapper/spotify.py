from . import sp


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
                data = {'name': song_name, 'artist': artist, 'URL': song_url, 'midi_title': title}
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