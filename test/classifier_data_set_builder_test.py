import csv
import pytest
import pandas as pd
from betel import classifier_data_set_builder
from betel import utils

CSV = """app_id,category
com.example,example
com.test,test
com.play,play
com.store,store
com.page,page"""

APP_LIST = pd.DataFrame(csv.DictReader(CSV.splitlines()))

SPLIT = {'train': pd.DataFrame([{'app_id': 'com.example', 'category': 'example'},
                                {'app_id': 'com.page', 'category': 'page'},
                                {'app_id': 'com.store', 'category': 'store'}]),
         'validation': pd.DataFrame([{'app_id': 'com.play', 'category': 'play'}]),
         'test': pd.DataFrame([{'app_id': 'com.test', 'category': 'test'}])}


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


@pytest.fixture
def storage_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("storage_dir")


@pytest.fixture
def classifier_builder(input_dir, storage_dir):
    return classifier_data_set_builder.ClassifierDataSetBuilder(input_dir, storage_dir)


class TestClassifierDataSetBuilder:
    def test_split(self, classifier_builder):
        split = classifier_builder.split(APP_LIST)

        sorted_split = {}
        for data_set in split:
            sorted_split[data_set] = split[data_set].sort_values(by=["app_id"])

        assert not all(split[data_set].equals(sorted_split[data_set]) for data_set in split)

    def test_expected_locations(self, classifier_builder, input_dir, storage_dir, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)
        expected_icons = _get_expected_icons(storage_dir)

        classifier_builder.split_and_build_data_sets()

        assert all(icon.exists() for icon in expected_icons)

    def test_expected_locations_with_classes(self, input_dir, storage_dir, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        classes = ["example"]

        _create_icons(APP_LIST, input_dir)
        expected_icons = _get_expected_icons(storage_dir, classes)

        classifier_builder = classifier_data_set_builder.ClassifierDataSetBuilder(
            input_dir, storage_dir, classes=classes
        )

        classifier_builder.split_and_build_data_sets()

        assert all(icon.exists() for icon in expected_icons)

    def test_info_file_content(self, classifier_builder, input_dir, storage_dir, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        expected_info = _get_expected_info(storage_dir)

        _create_icons(APP_LIST, input_dir)

        classifier_builder.split_and_build_data_sets()

        assert all(info["info"] in info["file"].read_text() for info in expected_info)


def _create_icons(app_list, input_dir):
    for _, app in app_list.iterrows():
        icon_name = utils.get_app_icon_name(app["app_id"])
        (input_dir / icon_name).touch()


def _get_expected_icons(storage_dir, classes=None):
    expected_icons = []
    for data_set in SPLIT:
        for _, app in SPLIT[data_set].iterrows():
            icon_name = utils.get_app_icon_name(app["app_id"])
            category = app["category"]
            if classes is not None:
                category = category if category in classes else "others"
            expected_location = storage_dir / data_set / category
            expected_icons.append(expected_location / icon_name)
    return expected_icons


def _get_expected_info(storage_dir):
    expected_info = []
    for data_set in SPLIT:
        for _, app in SPLIT[data_set].iterrows():
            file = storage_dir / "info" / app["category"]
            app_id = app["app_id"]
            info = f"{app_id},{data_set}"
            expected_info.append({"file": file, "info": info})
    return expected_info
