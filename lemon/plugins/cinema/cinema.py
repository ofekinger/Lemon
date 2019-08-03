class BaseCinema:
    def __init__(self, name):
        self.name = name

    def get_movies(self, date):
        raise NotImplementedError()

    def get_screenings(self, movie_name, date):
        raise NotImplementedError()


class MovieInfo:
    def __init__(self, name, poster, trailer, attributes):
        self.name = name
        self.poster = poster
        self.trailer = trailer
        self.attributes = attributes


class ScreeningInfo:
    def __init__(self, time, link, attributes, cinema=None, extra_info=None, movie=None):
        self.time = time
        self.link = link
        self.attributes = attributes
        self.cinema = cinema
        self.extra_info = extra_info
        self.movie = movie
