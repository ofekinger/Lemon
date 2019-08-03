from datetime import datetime

from lemon.plugins.cinema.cinema import BaseCinema, MovieInfo, ScreeningInfo
import requests
from bs4 import BeautifulSoup, NavigableString

from lemon.plugins.cinema.yes_planet_cinema import APIResult


class HotCinema(BaseCinema):
    DATA_API = "https://hotcinema.co.il/theatre_list.aspx?theatresid={cinema_id}&eventdate={date}"
    POSTER_URL = "https://hotcinema.co.il{poster_url}"
    ORDER_URL = "https://hotcinema.co.il/purchase.aspx?theatreid={ticket_theatre_id}&eventid={event_id}"

    def __init__(self, name, cinema_id, ticket_theatre_id):
        self.__cinema_id = cinema_id
        self.__ticket_theatre_id = ticket_theatre_id
        super(HotCinema, self).__init__(name=name)

    def get_movies(self, date):
        return self.__query_website(date).films

    def get_screenings(self, movie_name, date):
        return self.__query_website(date, movie_name).events

    def __query_website(self, date, movie_name=None):
        web_response = requests.get(self.DATA_API.format(cinema_id=self.__cinema_id,
                                                         date=date.strftime("%d/%m/%Y")))
        soup = BeautifulSoup(web_response.content)
        soup_movies = soup.find("div").find("table").find_all("tr", class_="yeshover")
        movies = []
        movie_screenings = []
        for movie in soup_movies:
            parsed_movie = MovieInfo(
                name=list(movie.find("td", class_="movie_name_list").find("a").children)[0],
                poster=self.POSTER_URL.format(poster_url=movie.find("td", class_="rela")
                                              .find("div", class_="poster_popup").find("div")
                                              .find("img").get("src").split("&")[0]),
                trailer=None,
                attributes=[attribute for attribute in movie.find("td", class_="sign pm").contents
                            if type(attribute) == NavigableString]
            )
            movies.append(parsed_movie)

            if parsed_movie.name == movie_name:
                hours = movie.find_all("td", class_="hour")
                for hour in hours:
                    movie_hour = hour.find("div").find("span").contents
                    event_id = hour.find("div").get("data-eventid")
                    if len(movie_hour) > 0:
                        movie_screenings.append(ScreeningInfo(
                            datetime.strptime(date.strftime("%Y/%m/%d {time}".format(time=movie_hour[0])),
                                              "%Y/%m/%d %H:%M"),
                            link=self.ORDER_URL.format(ticket_theatre_id=self.__ticket_theatre_id,
                                                       event_id=event_id),
                            attributes=parsed_movie.attributes,
                            extra_info=" ".join(parsed_movie.attributes),
                            movie=parsed_movie
                        ))

        return APIResult(movies, movie_screenings)
