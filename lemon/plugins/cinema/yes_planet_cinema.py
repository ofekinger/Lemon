from datetime import datetime

import requests

from lemon.plugins.cinema.cinema import BaseCinema, MovieInfo, ScreeningInfo


DUBBED_STRING = "מדובב"
SUBBED_STRING = "כתוביות"


class APIResult:
    def __init__(self, films, events):
        self.films = films
        self.events = events


class YesPlanetCinema(BaseCinema):
    DATA_API = "https://www.yesplanet.co.il/il/data-api-service/v1/quickbook/" \
               "10100/film-events/in-cinema/{cinema_id}/at-date/{date}"

    def __init__(self, name, cinema_id):
        self.__cinema_id = cinema_id
        super(YesPlanetCinema, self).__init__(name=name)

    def get_movies(self, date):
        result = self.__query_api(date)

        return [
            MovieInfo(
                name=movie["name"],
                poster=movie["posterLink"],
                trailer=movie["videoLink"],
                attributes=movie["attributeIds"]
            )
            for movie in result.films
        ]

    def get_screenings(self, movie_name, date):
        result = self.__query_api(date)
        movie_id = None
        for movie in result.films:
            if movie["name"] == movie_name:
                movie_id = movie["id"]
                break

        events = []
        if movie_id:
            for event in result.events:
                if event["filmId"] == movie_id:
                    events.append(
                        ScreeningInfo(
                            time=datetime.fromisoformat(event["eventDateTime"]),
                            link=event["bookingLink"],
                            attributes=event["attributeIds"],
                            extra_info=DUBBED_STRING if "dubbed" in event["attributeIds"] else SUBBED_STRING
                        )
                    )

        return events

    def __query_api(self, date: datetime):
        parsed_date = date.strftime("%Y-%m-%d")
        api_response = requests.get(self.DATA_API.format(cinema_id=self.__cinema_id,
                                                         date=parsed_date))

        if api_response.status_code != 200:
            raise requests.exceptions.HTTPError("Got {} status code when reaching {}".format(
                requests.status_codes.codes.get(api_response.status_code),
                self.name
            ))

        api_response = api_response.json()

        movies = api_response["body"]["films"]
        events = api_response["body"]["events"]

        return APIResult(movies, events)
