from pathlib import Path
import pytest
from src import PlayScrapingError, PlayAppPageScraper, AccessError

ICON_HTML = """
<img src="%s" class="T75of sHb2Xb">
"""

CATEGORY_HTML = """
<a itemprop="genre">Example</a>
"""

SIMPLE_HTML = """
<p>Simple paragraph.</p>
"""

ICON_SUBDIR = Path("icon_subdir")
APP_ID = "com.example"
ICON_NAME = "icon_com.example"

FILE = "file:"


@pytest.fixture
def icon_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("icon_dir")


@pytest.fixture
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_dir")


@pytest.fixture
def play_scraper(icon_dir, test_dir):
    base_url = FILE + str(test_dir) + "/"
    return PlayAppPageScraper(base_url, icon_dir)


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


class TestAppPageScraper:
    def test_get_icon(self, test_dir, icon_dir, play_scraper):
        rand_array = _create_icon(test_dir)

        _create_html_file(test_dir, ICON_HTML, icon_html=True)

        play_scraper.get_app_icon(APP_ID, ICON_SUBDIR)

        read_icon = icon_dir / ICON_SUBDIR / ICON_NAME
        read_array = read_icon.read_text()
        assert read_array == rand_array

    def test_get_category(self, play_scraper, test_dir):
        expected_genre = "example"

        _create_html_file(test_dir, CATEGORY_HTML)

        genre = play_scraper.get_app_category(APP_ID)

        assert genre == expected_genre

    def test_missing_icon_class(self, play_scraper, test_dir):
        _create_html_file(test_dir, SIMPLE_HTML)

        with pytest.raises(PlayScrapingError) as exc:
            play_scraper.get_app_icon(APP_ID, ICON_SUBDIR)

        assert str(exc.value) == "Icon class not found in html."

    def test_missing_category_itemprop(self, play_scraper, test_dir):
        _create_html_file(test_dir, SIMPLE_HTML)

        with pytest.raises(PlayScrapingError) as exc:
            play_scraper.get_app_category(APP_ID)

        assert str(exc.value) == "Category itemprop not found in html."

    def test_invalid_base_url(self, icon_dir):
        random_url = "https://127.0.0.1/betel-test-invalid-base-url-835AHD/"

        play_scraper = PlayAppPageScraper(random_url, icon_dir)

        with pytest.raises(AccessError):
            play_scraper.get_app_category("com.invalid.base.url")

    def test_invalid_icon_url(self, play_scraper, test_dir):
        _create_html_file(test_dir, ICON_HTML, icon_html=True)

        with pytest.raises(AccessError):
            play_scraper.get_app_icon("com.invalid.icon.url")


def _create_html_file(test_dir, text, icon_html=False):
    html_file = test_dir / "details?id=com.example"

    if icon_html:
        html_img_src = FILE + str(test_dir / ICON_NAME)
        text = text % html_img_src

    html_file.write_text(text)


def _create_icon(test_dir):
    rand_array = str([15, 934, 8953, 409, 32])
    rand_icon = test_dir / ICON_NAME
    rand_icon.write_text(rand_array)
    return rand_array
