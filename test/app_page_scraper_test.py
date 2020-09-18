import pathlib
import pytest
from betel import app_page_scraper
from betel import betel_errors
from betel import utils

ICON_HTML = """
<img src="%s" class="T75of sHb2Xb">
"""

CATEGORY_HTML = """
<a itemprop="genre">Example</a>
"""

FILTERED_CATEGORY_HTML = """
<a itemprop="genre">Filtered</a>
"""

SIMPLE_HTML = """
<p>Simple paragraph.</p>
"""

ICON_SUBDIR = pathlib.Path("icon_subdir")
APP_ID = "com.example"
ICON_NAME = "icon_com.example"
EXPECTED_CATEGORY = "example"

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
    return app_page_scraper.PlayAppPageScraper(base_url, icon_dir, ["example"])


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


class TestAppPageScraper:
    def test_get_icon(self, play_scraper, test_dir, icon_dir):
        rand_icon = _create_icon(test_dir)

        _create_html_file(test_dir, ICON_HTML, icon_src=True)

        play_scraper.get_app_icon(APP_ID, ICON_SUBDIR)

        read_icon = icon_dir / ICON_SUBDIR / ICON_NAME

        assert read_icon.exists()
        assert read_icon.read_text() == rand_icon.read_text()

    def test_get_category(self, play_scraper, test_dir):
        _create_html_file(test_dir, CATEGORY_HTML)

        genre = play_scraper.get_app_category(APP_ID)

        assert genre == EXPECTED_CATEGORY

    def test_missing_icon_class(self, play_scraper, test_dir):
        _create_html_file(test_dir, SIMPLE_HTML)

        with pytest.raises(betel_errors.PlayScrapingError) as exc:
            play_scraper.get_app_icon(APP_ID, ICON_SUBDIR)

        assert str(exc.value) == "Icon class not found in html."

    def test_missing_category_itemprop(self, play_scraper, test_dir):
        _create_html_file(test_dir, SIMPLE_HTML)

        with pytest.raises(betel_errors.PlayScrapingError) as exc:
            play_scraper.get_app_category(APP_ID)

        assert str(exc.value) == "Category itemprop not found in html."

    def test_invalid_base_url(self, icon_dir):
        random_url = "https://127.0.0.1/betel-test-invalid-base-url-835AHD/"

        play_scraper = app_page_scraper.PlayAppPageScraper(random_url, icon_dir)

        with pytest.raises(betel_errors.AccessError) as exc:
            play_scraper.get_app_category(APP_ID)

        assert "Can not open URL." in str(exc.value)

    def test_invalid_icon_url(self, play_scraper, test_dir):
        _create_html_file(test_dir, ICON_HTML, icon_src=True)

        with pytest.raises(betel_errors.AccessError) as exc:
            play_scraper.get_app_icon(APP_ID)

        assert "Can not retrieve icon." in str(exc.value)

    def test_store_app_info(self, play_scraper, test_dir, icon_dir):
        expected_info = f"{APP_ID},{EXPECTED_CATEGORY}"

        _create_html_file(test_dir, ICON_HTML + CATEGORY_HTML, icon_src=True)
        rand_icon = _create_icon(test_dir)

        play_scraper.store_app_info(APP_ID)

        retrieved_icon = icon_dir / ICON_NAME
        info_file = icon_dir / utils.SCRAPER_INFO_FILE_NAME

        assert retrieved_icon.exists()
        assert rand_icon.read_text() == retrieved_icon.read_text()
        assert expected_info in info_file.read_text()

    def test_store_app_info_filter(self, play_scraper, test_dir, icon_dir):
        _create_html_file(test_dir, ICON_HTML + FILTERED_CATEGORY_HTML, icon_src=True)
        _create_icon(test_dir)

        play_scraper.store_app_info(APP_ID)

        retrieved_icon = icon_dir / ICON_NAME

        assert not retrieved_icon.exists()


def _create_html_file(test_dir, text, icon_src=False):
    html_file = test_dir / "details?id=com.example"

    if icon_src:
        html_img_src = FILE + str(test_dir / ICON_NAME)
        text = text % html_img_src

    html_file.write_text(text)


def _create_icon(test_dir):
    rand_array = str([15, 934, 8953, 409, 32])
    rand_icon = test_dir / ICON_NAME
    rand_icon.write_text(rand_array)

    return rand_icon
