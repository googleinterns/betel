from urllib.request import urlopen, urlretrieve
import os
from bs4 import BeautifulSoup


class PlayPageScraper:
    """A class for scraping Google Play Store web pages.

    Attributes:
        _base_url: str
            Base url of the app's web pages.
        _storage_dir: str
            The main storage directory for retrieved info.
    """

    ICON_CLASS = "T75of sHb2Xb"

    def __init__(self, base_url, storage_dir):
        self._base_url = base_url

        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)
        self._storage_dir = storage_dir

    def __get_html(self, app_id, language=None):
        """Obtains the html of the app's web page.

        :param app_id (str): the id of the app.
        :param language (str): app's language.
        :return: a BeautifulSoup object containing the html.
        """
        url = self._base_url + app_id

        if language is not None:
            url += "&hl=" + language

        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_icon(self, app_id, language=None, directory=""):
        """Downloads the app's icon from the corresponding web page.

        :param app_id (str): the id of the app.
        :param language (str): app's language.
        :param directory (str): icon storage subdirectory.
        """
        html = self.__get_html(app_id, language)

        icon = html.find(class_=self.ICON_CLASS)
        src = icon["src"]

        location = self._storage_dir + directory
        if directory and not os.path.exists(location):
            os.mkdir(location)

        _, _ = urlretrieve(src, location + "icon_" + app_id)
