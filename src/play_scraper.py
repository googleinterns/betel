from urllib.request import urlopen, urlretrieve
from pathlib import Path
from bs4 import BeautifulSoup


def _get_html(url: str) -> BeautifulSoup:
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


class PlayPageScraper:
    """A class for scraping Google Play Store web pages."""

    _ICON_CLASS = "T75of sHb2Xb"  # icon's tag's class
    _CATEGORY_ITEMPROP = "genre"  # category's tag's itemprop

    def __init__(self, base_url: str, storage_dir: Path):
        """Constructor.

        :param base_url: base url of the apps' web pages.
        :param storage_dir: main storage directory for retrieved info.
        """
        self._base_url = base_url

        self._storage_dir = storage_dir
        self._storage_dir.mkdir(exist_ok=True, parents=True)

    def get_icon(self, app_id: str, directory: Path = "") -> None:
        """Downloads the app's icon from the corresponding web page.

        :param app_id: the id of the app.
        :param directory: icon storage subdirectory.
        """
        url = self._base_url + app_id
        html = _get_html(url)

        icon = html.find(class_=self._ICON_CLASS)
        src = icon["src"]

        location = self._storage_dir / directory
        location.mkdir(exist_ok=True)

        urlretrieve(src, location / f"icon_{app_id}")

    def get_category(self, app_id: str) -> str:
        """Scrapes app's category.

        :param app_id: the id of the app.
        :return: the category of the app in str format
        """
        url = self._base_url + app_id
        html = _get_html(url)

        category = html.find(itemprop=self._CATEGORY_ITEMPROP)
        return category.get_text().lower()
