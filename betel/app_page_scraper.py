import pathlib
import urllib.error
import urllib.request
import logging
import bs4
import parmap
import pandas as pd
from betel import utils
from betel import info_files_helpers
from betel import betel_errors


class PlayAppPageScraper:
    """A class for scraping the icons and categories from Google Play Store
    apps' web pages."""

    _ICON_CLASS = "T75of sHb2Xb"  # icon's tag's class
    _APP_CATEGORY_ITEMPROP = "genre"  # app's category's tag's itemprop

    def __init__(self, base_url: str, storage_dir: pathlib.Path, category_filter: [str] = None):
        """Constructor.

        :param base_url: base url of the apps store.
        :param storage_dir: main storage directory for retrieved info.
        :param category_filter: a list of categories whose apps are stored
        (instead of the whole input)
        """
        self._base_url = base_url

        self._storage_dir = storage_dir
        self._storage_dir.mkdir(exist_ok=True, parents=True)

        self._info_file = storage_dir / utils.SCRAPER_INFO_FILE_NAME

        self._log_file = storage_dir / utils.SCRAPER_LOG_FILE_NAME
        logging.basicConfig(filename=self._log_file, filemode="a+")

        self._category_filter = category_filter

    def _build_app_page_url(self, app_id: str) -> str:
        return self._base_url + "/details?id=" + app_id

    def _get_app_page(self, app_id: str) -> bs4.BeautifulSoup:
        url = self._build_app_page_url(app_id)
        return _get_html(url)

    def get_app_icon(self, app_id: str, subdir: pathlib.Path = "") -> None:
        """Scrapes the app icon URL from the app's Play Store details page,
        downloads the corresponding app icon and saves it to
        _storage_dir / subdir /  icon_{app_id}.

        :param app_id: the id of the app.
        :param subdir: icon storage subdirectory inside _storage_dir base
        directory.
        """
        html = self._get_app_page(app_id)
        src = self._scrape_icon_url(html)
        self._download_icon(app_id, src, subdir)

    def _scrape_icon_url(self, html: bs4.BeautifulSoup) -> str:
        icon = html.find(class_=self._ICON_CLASS)
        if icon is None:
            raise betel_errors.PlayScrapingError("Icon class not found in html.")
        return icon["src"]

    def _download_icon(self, app_id: str, source: str, directory: pathlib.Path) -> None:
        location = self._storage_dir / directory
        location.mkdir(exist_ok=True, parents=True)

        try:
            urllib.request.urlretrieve(source, location / utils.get_app_icon_name(app_id))
        except (urllib.error.HTTPError, urllib.error.URLError) as exception:
            raise betel_errors.AccessError("Can not retrieve icon.", exception)

    def get_app_category(self, app_id: str) -> str:
        """Scrapes the app category from the app's Play Store details page.

        :param app_id: the id of the app.
        :return: the category of the app in str format
        """
        html = self._get_app_page(app_id)
        return self._scrape_category(html).lower()

    def _scrape_category(self, html: bs4.BeautifulSoup) -> str:
        category = html.find(itemprop=self._APP_CATEGORY_ITEMPROP)
        if category is None:
            raise betel_errors.PlayScrapingError("Category itemprop not found in html.")
        return category.get_text()

    def store_app_info(self, app_id: str) -> None:
        """Adds an app to the data set by retrieving all the info
        needed and appending it to the list of apps (kept in _info_file).
        The app is only stored in the case that its category is in the
        _category_filter list.

        :param app_id: the id of the app.
        """
        search_data_frame = utils.get_app_search_data_frame(app_id)
        part_of_data_set = (
            info_files_helpers.part_of_data_set(self._info_file, search_data_frame)
        )

        try:
            if not part_of_data_set:
                category = self.get_app_category(app_id)
                if self._category_filter is None or category in self._category_filter:
                    self.get_app_icon(app_id)
                    self._write_app_info(app_id, category)
        except betel_errors.BetelError as exception:
            info = f"{app_id}, {getattr(exception, 'message', repr(exception))}"
            logging.warning(info)

    def _write_app_info(self, app_id: str, category: str) -> None:
        app_info = _build_app_info_data_frame(app_id, category)
        info_files_helpers.add_to_data(self._info_file, app_info)

    def store_apps_info(self, app_ids: [str]) -> None:
        """Adds the specified apps to the data set by retrieving all the info
        needed and appending them to the list of apps (kept in _info_file).

        :param app_ids: array of app ids.
        """
        app_ids = set(app_ids)
        parmap.map(self.store_app_info, app_ids)


def _get_html(url: str) -> bs4.BeautifulSoup:
    try:
        page = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(page, 'html.parser')
        return soup
    except (urllib.error.HTTPError, urllib.error.URLError) as exception:
        raise betel_errors.AccessError("Can not open URL.", exception)


def _build_app_info_data_frame(app_id: str, category: str) -> pd.DataFrame:
    dictionary = {"app_id": app_id, "category": category}
    return pd.DataFrame([dictionary])
