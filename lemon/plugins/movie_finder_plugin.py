"""
Finds information about movies by querying cinema websites.


Movie:
    name
    genre
    screenings: {cinema: list(datetime)}

Cinema:
    name
    movies: {name: list(datetime)}

get_screenings_by_name
get_movies_by_cinema
get_cinemas_by_movie
"""
import logging
from datetime import datetime

import pytz

from lemon.plugins.base_plugin import BasePlugin, MenuOption
from lemon.plugins.cinema.hot_cinema import HotCinema
from lemon.plugins.cinema.rav_hen_cinema import RavHenCinema
from lemon.plugins.cinema.yes_planet_cinema import YesPlanetCinema


class MovieFinderPlugin(BasePlugin):
    NAME = "movie_finder"

    def __init__(self, database_communication):
        super(MovieFinderPlugin, self).__init__(database_communication)
        self.__cinemas = [
            YesPlanetCinema("יס פלאנט - איילון", "1025"),
            YesPlanetCinema("יס פלאנט - ראשון לציון", "1072"),
            RavHenCinema("רב חן - קריית אונו", "1062"),
            HotCinema("הוט סינמה - פתח תקווה", "14", "1194"),
            HotCinema("הוט סינמה - כפר סבא", "16", "1197"),
            RavHenCinema("רב חן - גבעתיים", "1058"),
            RavHenCinema("רב חן - דיזינגוף", "1071")
        ]

    def _execute(self):
        movies = {}
        date = datetime.now(tz=pytz.UTC).astimezone(pytz.timezone("Asia/Jerusalem"))
        cinema_movies = {cinema: cinema.get_movies(date=date) for cinema in self.__cinemas}

        for cinema, presenting_movies in cinema_movies.items():
            logging.debug("{} presents: {}".format(cinema.name, [movie.name for movie in presenting_movies]))
            movies.update({movie.name: movie for movie in presenting_movies if movie.name not in movies.keys()})

        movie_found = None
        for movie_name, movie in movies.items():
            if movie_name in self.arguments:
                movie_found = movie

        if movie_found:
            self.__send_poster(cinema_movies.values(), movie_found.name)
            self.__send_trailer(cinema_movies.values(), movie_found.name)

            # Send dates
            self.__handle_screenings(movie_found.name, date)
        else:
            self._build_menu(options=[MenuOption(movie_name) for movie_name in movies.keys()],
                             text="Pick one movie:",
                             reply_prefix=self.NAME)

    def __handle_screenings(self, movie_name, date):
        screenings = []
        for cinema in self.__cinemas:
            cinema_screenings = cinema.get_screenings(movie_name, date=date)
            for screening in cinema_screenings:
                screening.cinema = cinema

            screenings += cinema_screenings

        screenings = sorted(screenings, key=lambda screening: screening.time)
        self._build_menu([MenuOption("{cinema_name} - {time} ({extra})".format(cinema_name=screening.cinema.name,
                                                                               time=screening.time.strftime("%H:%M"),
                                                                               extra=screening.extra_info),
                                     url=screening.link)
                          for screening in screenings], "Pick a screening:")

    def __send_poster(self, all_movies, movie_name):
        for movie_list in all_movies:
            for movie in movie_list:
                if movie.name == movie_name:
                    try:
                        self._send_photo(movie.poster)
                    except Exception:
                        break
                    else:
                        return

    def __send_trailer(self, all_movies, movie_name):
        for movie_list in all_movies:
            for movie in movie_list:
                if movie.name == movie_name:
                    if movie.trailer is None:
                        break

                    try:
                        self._send_text_message(movie.trailer)
                    except Exception:
                        break
                    else:
                        return
