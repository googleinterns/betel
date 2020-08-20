from pathlib import Path
from urllib.error import HTTPError, URLError
import numpy as np
import pytest
from src import PlayScrapingError, PlayPageScraper

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


class TestPlayPageScraper:
    def test_get_icon(self, test_dir, icon_dir, play_scraper):
        rand_array = np.random.randint(0, 255, 10)
        icon_name = "icon_com.example"
        np.savetxt(test_dir / icon_name, rand_array, fmt="%d")

        html_file = test_dir / "com.example"
        html_img_src = pytest.FILE + str(test_dir / icon_name)
        html_file.write_text(ICON_HTML % html_img_src)

        play_scraper.get_icon("com.example", ICON_SUBDIR)

        read_array = np.loadtxt(icon_dir / ICON_SUBDIR / icon_name, dtype=int)
        assert np.array_equal(rand_array, read_array)

    def test_get_category(self, play_scraper, test_dir):
        expected_genre = "example"

        html_file = test_dir / "com.example.bis"
        html_file.write_text(CATEGORY_HTML)

        genre = play_scraper.get_category("com.example.bis")

        assert expected_genre == genre

    def test_missing_icon_class(self, play_scraper, test_dir):
        html_file = test_dir / "com.class.error"
        html_file.write_text(SIMPLE_HTML)

        with pytest.raises(PlayScrapingError) as exc:
            play_scraper.get_icon("com.class.error", ICON_SUBDIR)

        assert str(exc.value) == "Icon class not found in html."

    def test_missing_category_itemprop(self, play_scraper, test_dir):
        html_file = test_dir / "com.itemprop.error"
        html_file.write_text(SIMPLE_HTML)

        with pytest.raises(PlayScrapingError) as exc:
            play_scraper.get_category("com.itemprop.error")

        assert str(exc.value) == "Category itemprop not found in html."

    def test_invalid_base_url(self, icon_dir):
        random_int = np.random.randint(10000)
        random_url = "https://127.0.0.1/" + str(random_int) + "/"

        play_scraper = PlayPageScraper(random_url, icon_dir)

        with pytest.raises((URLError, HTTPError)):
            play_scraper.get_category("com.invalid.base.url")

    def test_invalid_icon_url(self, play_scraper, test_dir):
        html_file = test_dir / "com.example"
        html_img_src = pytest.FILE + str(test_dir / "icon_name")
        html_file.write_text(ICON_HTML % html_img_src)

        with pytest.raises((URLError, HTTPError)):
            play_scraper.get_icon("com.invalid.icon.url")
