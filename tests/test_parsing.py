import requests
from bs4 import BeautifulSoup

from bot.main import parse_series


class MockResponse:
    def __init__(self, content):
        self.content = content


def test_parse_valid_series(monkeypatch):
    series_data = BeautifulSoup(
        """
    <html><body>
    <article class="item tvshows" id="post-42">
        <div class="poster"><img alt="series_title" src="some_image">
            <div class="rating" id="tmdb">6</div>
            <div class="mepo"></div>
            <a href="title_url" title="some_title">
                <div class="see play2"></div>
            </a>
            4
        </div>
        <div class="data">
            <h3>
                <a href="data_url" title="some_other_title">Series title</a>
            </h3>
            <span>Dec. 25, 2022</span>
        </div>
    </article>
    </body></html>"""
    )

    description_data = b"""
    <html><body>
    <span class="country">
    <a href="some_first_url" rel="tag">First Genre</a>
    <a href="some_second_url" rel="tag">Second Genre</a>
    </span>
    <div class="wp-content" id="wp-content">
        <p>First paragraph</p>
        <p>Second paragraph</p>
    </div>
    </body></html>"""

    def mock_get(*args, **kwargs):
        return MockResponse(description_data)

    monkeypatch.setattr(requests, "get", mock_get)

    result = parse_series(series_data)

    assert (
        result == "Series title"
        "\n6"
        "\nFirst Genre,Second Genre"
        "\nFirst paragraph"
        "\nSecond paragraph"
        "\ntitle_url"
    )
