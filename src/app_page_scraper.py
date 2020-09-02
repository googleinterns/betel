from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
from .utils import get_app_icon_name, SCRAPER_INFO_FILE_NAME
from .betel_errors import PlayScrapingError, AccessError


class PlayAppPageScraper:
    """A class for scraping the icons and categories from Google Play Store
    apps' web pages."""

    _ICON_CLASS = "T75of sHb2Xb"  # icon's tag's class
    _APP_CATEGORY_ITEMPROP = "genre"  # app's category's tag's itemprop

    def __init__(self, base_url: str, storage_dir: Path):
        """Constructor.

        :param base_url: base url of the apps store.
        :param storage_dir: main storage directory for retrieved info.
        """
        self._base_url = base_url

        self._storage_dir = storage_dir
        self._storage_dir.mkdir(exist_ok=True, parents=True)

        self._info_file = storage_dir / SCRAPER_INFO_FILE_NAME

    def _build_app_page_url(self, app_id: str) -> str:
        return self._base_url + "/details?id=" + app_id

    def _get_app_page(self, app_id: str) -> BeautifulSoup:
        url = self._build_app_page_url(app_id)
        return _get_html(url)

    def get_app_icon(self, app_id: str, subdir: Path = "") -> None:
        """Scrapes the app icon URL from the app's Play Store details page,
        downloads the corresponding app icon and saves it to
        _storage_dir / subdir / icon_{app_id}.

        :param app_id: the id of the app.
        :param subdir: icon storage subdirectory inside _storage_dir base
        directory.
        """
        html = self._get_app_page(app_id)
        src = self._scrape_icon_url(html)
        self._download_icon(app_id, src, subdir)

    def _scrape_icon_url(self, html: BeautifulSoup) -> str:
        icon = html.find(class_=self._ICON_CLASS)
        if icon is None:
            raise PlayScrapingError("Icon class not found in html.")
        return icon["src"]

    def _download_icon(self, app_id: str, src: str, directory: Path) -> None:
        location = self._storage_dir / directory
        location.mkdir(exist_ok=True, parents=True)

        try:
            urlretrieve(src, location / get_app_icon_name(app_id))
        except (HTTPError, URLError) as exception:
            raise AccessError("Can not retrieve icon", exception)

    def get_app_category(self, app_id: str) -> str:
        """Scrapes the app category from the app's Play Store details page.

        :param app_id: the id of the app.
        :return: the category of the app in str format
        """
        html = self._get_app_page(app_id)
        return self._scrape_category(html).lower()

    def _scrape_category(self, html: BeautifulSoup) -> str:
        category = html.find(itemprop=self._APP_CATEGORY_ITEMPROP)
        if category is None:
            raise PlayScrapingError("Category itemprop not found in html.")
        return category.get_text()


def _get_html(url: str) -> BeautifulSoup:
    try:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup
    except (HTTPError, URLError) as exception:
        raise AccessError("Can not open URL", exception)
