from lemon.plugins.cinema.yes_planet_cinema import YesPlanetCinema


class RavHenCinema(YesPlanetCinema):
    DATA_API = "https://www.rav-hen.co.il/rh/data-api-service/v1/quickbook/" \
               "10104/film-events/in-cinema/{cinema_id}/at-date/{date}"
