import pytest
from src import PlayAppPageScraper


def pytest_configure():
    pytest.FILE = "file:"


@pytest.fixture
def icon_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("icon_dir")


@pytest.fixture
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_dir")


@pytest.fixture
def play_scraper(icon_dir, test_dir):
    base_url = pytest.FILE + str(test_dir) + "/"
    return PlayAppPageScraper(base_url, icon_dir)
