from pathlib import Path
import numpy as np

ICON_HTML = """
<img src="file:%s/icon_com.example" class="T75of sHb2Xb">
"""

CATEGORY_HTML = """
<a itemprop="genre">Example</a>
"""


class TestPlayPageScraper:
    def test_get_icon(self, test_dir, icon_dir, play_scraper):
        rand_array = np.random.randint(0, 255, 10)
        file_name = "icon_com.example"
        np.savetxt(test_dir / file_name, rand_array, fmt="%d")

        html_file = test_dir / "com.example"
        html_file.write_text(ICON_HTML % test_dir)

        icon_subdir = Path("icon_subdir")
        play_scraper.get_icon("com.example", directory=icon_subdir)

        read_array = np.loadtxt(icon_dir / icon_subdir / file_name, dtype=int)
        assert np.array_equal(rand_array, read_array)

    def test_get_category(self, play_scraper, test_dir):
        expected_genre = "example"

        html_file = test_dir / "com.example.bis"
        html_file.write_text(CATEGORY_HTML)

        genre = play_scraper.get_category("com.example.bis")

        assert expected_genre == genre
