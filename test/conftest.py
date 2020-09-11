import pytest
import PIL
from src import PlayAppPageScraper, BetelClassifierSequence


def pytest_configure():
    pytest.FILE = "file:"
    pytest.batch_size = 4
    pytest.target_input_size = (192, 192)


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


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


@pytest.fixture
def icons(input_dir):
    icons = []
    for index in range(3):
        category_dir = input_dir / f"category{index}"
        category_dir.mkdir()

        for icon_index in range(index + 1):
            icon = category_dir / f"icon_{icon_index}"
            icon.touch()
            image = PIL.Image.new('RGBA', size=(180, 180))
            image.save(icon, 'png')
            icons.append((icon.name, category_dir.name))

    return icons


@pytest.fixture
def classifier_sequence(input_dir, icons):
    return BetelClassifierSequence(
        input_dir,
        pytest.batch_size,
    )
