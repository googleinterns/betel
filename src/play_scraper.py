from urllib.request import urlopen, urlretrieve
from pathlib import Path
from bs4 import BeautifulSoup


def _get_html(url: str) -> BeautifulSoup:
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


class PlayScrapingError(Exception):
    """Raise when certain attributes can't be found within the Play page."""


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

    def _build_app_page_url(self, app_id: str) -> str:
        return self._base_url + app_id

    def _get_details_page(self, app_id: str) -> BeautifulSoup:
        url = self._build_app_page_url(app_id)
        return _get_html(url)

    def _scrape_icon_url(self, html: BeautifulSoup) -> str:
        icon = html.find(class_=self._ICON_CLASS)
        if icon is None:
            raise PlayScrapingError("Icon class not found in html.")
        return icon["src"]

    def _download_icon(self, app_id: str, src: str, directory: Path) -> None:
        location = self._storage_dir / directory
        location.mkdir(exist_ok=True, parents=True)

        urlretrieve(src, location / f"icon_{app_id}")

    def _scrape_category(self, html: BeautifulSoup) -> str:
        category = html.find(itemprop=self._CATEGORY_ITEMPROP)
        if category is None:
            raise PlayScrapingError("Category itemprop not found in html.")
        return category.get_text()

    def get_icon(self, app_id: str, directory: Path = "") -> None:
        """Scrapes the app icon URL from the app's Play Store details page,
        downloads the corresponding app icon and saves it to the specified
        subdirectory.

        :param app_id: the id of the app.
        :param directory: icon storage subdirectory inside _storage_dir base
        directory.
        """
        html = self._get_details_page(app_id)
        src = self._scrape_icon_url(html)
        self._download_icon(app_id, src, directory)

    def get_category(self, app_id: str) -> str:
        """Scrapes the app category from the app's Play Store details page.

        :param app_id: the id of the app.
        :return: the category of the app in str format
        """
        html = self._get_details_page(app_id)
        return self._scrape_category(html).lower()
