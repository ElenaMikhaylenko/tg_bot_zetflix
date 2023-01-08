import requests
from bs4 import BeautifulSoup

URL = "https://зетфликсс.online/tvshows/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
}


def get_new_series(last_known_post_series_id):
    soup = BeautifulSoup(
        requests.get(URL, headers=HEADERS).content, "html.parser"
    )

    last_post_series = soup.find(
        "article", class_="item tvshows", id=True
    )  # posted?
    last_post_series_id = last_post_series["id"]

    if last_post_series_id != last_known_post_series_id:
        return parse_series(last_post_series), last_post_series_id
    return None, None


def parse_series(last_post_series):
    title = last_post_series.find("div", class_="data").find("a").text
    rating = last_post_series.find("div", class_="rating").text

    description_url = last_post_series.find("a").get("href")
    description_data = BeautifulSoup(
        requests.get(description_url, headers=HEADERS).content, "html.parser"
    )

    description = "\n".join(
        [
            description.text
            for description in description_data.find(
                "div", id="wp-content"
            ).find_all("p")
        ]
    )
    genre_film = [
        genre.text for genre in description_data.find_all("a", rel="tag")
    ]

    return f"{title}\n{rating}\n{','.join(genre_film)}\n{description}\n{description_url}"
