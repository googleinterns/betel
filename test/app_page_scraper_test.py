import pathlib
import pytest
from src import PlayScrapingError, PlayAppPageScraper, AccessError, SCRAPER_INFO_FILE_NAME

ICON_HTML = """
<img src="%s" class="T75of sHb2Xb">
"""

CATEGORY_HTML = """
<a itemprop="genre">Example</a>
"""

SIMPLE_HTML = """
<p>Simple paragraph.</p>
"""

ICON_SUBDIR = pathlib.Path("icon_subdir")
APP_ID = "com.example"
ICON_NAME = "icon_com.example"
EXPECTED_CATEGORY = "example"


class TestAppPageScraper:
    def test_get_icon(self, play_scraper, test_dir, icon_dir):
        rand_icon = _create_icon(test_dir)

        _create_html_file(test_dir, ICON_HTML, icon_src=True)

        play_scraper.get_app_icon(APP_ID, ICON_SUBDIR)

        read_icon = icon_dir / ICON_SUBDIR / ICON_NAME

        assert read_icon.exists()
        assert rand_icon.read_text() == read_icon.read_text()

    def test_get_category(self, play_scraper, test_dir):
        _create_html_file(test_dir, CATEGORY_HTML)

        genre = play_scraper.get_app_category(APP_ID)

        assert EXPECTED_CATEGORY == genre

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
        _create_html_file(test_dir, ICON_HTML, icon_src=True)

        with pytest.raises(AccessError):
            play_scraper.get_app_icon("com.invalid.icon.url")

    def test_store_app_info(self, play_scraper, test_dir, icon_dir):
        expected_info = f"{APP_ID},{EXPECTED_CATEGORY}"

        _create_html_file(test_dir, ICON_HTML + CATEGORY_HTML, icon_src=True)
        rand_icon = _create_icon(test_dir)

        play_scraper.store_app_info(APP_ID)

        retrieved_icon = icon_dir / ICON_NAME
        info_file = icon_dir / SCRAPER_INFO_FILE_NAME

        assert retrieved_icon.exists()
        assert rand_icon.read_text() == retrieved_icon.read_text()
        assert expected_info in info_file.read_text()


def _create_html_file(test_dir, text, icon_src=False):
    html_file = test_dir / "details?id=com.example"

    if icon_src:
        html_img_src = pytest.FILE + str(test_dir / ICON_NAME)
        text = text % html_img_src

    html_file.write_text(text)


def _create_icon(test_dir):
    rand_array = str([15, 934, 8953, 409, 32])
    rand_icon = test_dir / ICON_NAME
    rand_icon.write_text(rand_array)
    return rand_icon
