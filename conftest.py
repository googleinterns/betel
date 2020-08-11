import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--directory",
        action="store",
        default="./app_details/",
        help="Path to destination directory for icons"
    )
    parser.addoption(
        "--subdir",
        action="store",
        default="",
        help="Destination subdirectory for icon"
    )

@pytest.fixture
def directory(request):
    return request.config.getoption("--directory")

@pytest.fixture
def subdir(request):
    return request.config.getoption("--subdir")
