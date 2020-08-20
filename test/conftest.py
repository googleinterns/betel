import pytest
from src.play_scraper import PlayPageScraper


def pytest_configure():
    pytest.FILE = "file:"


@pytest.fixture(scope="session")
def icon_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("icon_dir")


@pytest.fixture(scope="session")
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_dir")


@pytest.fixture(scope="module")
def play_scraper(icon_dir, test_dir):
    base_url = pytest.FILE + str(test_dir) + "/"
    return PlayPageScraper(base_url, icon_dir)
