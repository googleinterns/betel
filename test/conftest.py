import pytest
from src.play_scraper import PlayPageScraper


@pytest.fixture(scope="session")
def icon_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("icon_dir")


@pytest.fixture(scope="session")
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_dir")


@pytest.fixture(scope="module")
def play_scraper(icon_dir, test_dir):
    return PlayPageScraper("file:" + str(test_dir) + "/", icon_dir)
