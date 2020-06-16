from . import ia


class IMDB(object):

    def __init__(self):
        pass

    @staticmethod
    def top250films():
        films = ia.get_top250_movies()
        film_ids = {}
        for film in films:
            film_id = film.movieID
            film_name = film['title']
            film_ids[film_id] = film_name
        return film_ids

    @staticmethod
    def get_movie_soundtrack(film_id):
        ost = ia.get_movie_soundtrack(film_id)
        return ost
