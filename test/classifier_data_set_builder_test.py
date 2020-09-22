import csv
import pytest
import pandas as pd
from betel import classifier_data_set_builder
from betel import utils

CSV = """app_id,category
com.example,example
com.test,example
com.play,play
com.store,store
com.page,page"""

APP_LIST = pd.DataFrame(csv.DictReader(CSV.splitlines()))

SPLIT = {'train': pd.DataFrame([{'app_id': 'com.example', 'category': 'example'},
                                {'app_id': 'com.page', 'category': 'page'},
                                {'app_id': 'com.store', 'category': 'store'}]),
         'validation': pd.DataFrame([{'app_id': 'com.play', 'category': 'play'}]),
         'test': pd.DataFrame([{'app_id': 'com.test', 'category': 'example'}])}

CLASSES = ["example", "play"]


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


@pytest.fixture
def storage_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("storage_dir")


@pytest.fixture
def classifier_builder(input_dir, storage_dir):
    return classifier_data_set_builder.ClassifierDataSetBuilder(input_dir, storage_dir)


@pytest.fixture
def expected_icons(storage_dir):
    return [
        storage_dir / "train" / "example" / "icon_com.example",
        storage_dir / "train" / "page" / "icon_com.page",
        storage_dir / "train" / "store" / "icon_com.store",
        storage_dir / "validation" / "play" / "icon_com.play",
        storage_dir / "test" / "example" / "icon_com.test"
    ]


@pytest.fixture
def expected_icons_when_classes_specified(storage_dir):
    return [
        storage_dir / "train" / "example" / "icon_com.example",
        storage_dir / "train" / "others" / "icon_com.page",
        storage_dir / "train" / "others" / "icon_com.store",
        storage_dir / "validation" / "play" / "icon_com.play",
        storage_dir / "test" / "example" / "icon_com.test"
    ]


@pytest.fixture
def expected_info(storage_dir):
    return [
        {"file": storage_dir / "info" / "example", "info": "com.example,train"},
        {"file": storage_dir / "info" / "page", "info": "com.page,train"},
        {"file": storage_dir / "info" / "store", "info": "com.store,train"},
        {"file": storage_dir / "info" / "play", "info": "com.play,validation"},
        {"file": storage_dir / "info" / "example", "info": "com.test,test"}
    ]


class TestClassifierDataSetBuilder:
    def test_split(self, classifier_builder):
        split = classifier_builder.split(APP_LIST)

        sorted_split = {}
        for data_set in split:
            sorted_split[data_set] = split[data_set].sort_values(by=["app_id"])

        assert not all(split[data_set].equals(sorted_split[data_set]) for data_set in split)

    def test_expected_locations(self, classifier_builder, input_dir, expected_icons, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder.split_and_build_data_sets()

        assert all(icon.exists() for icon in expected_icons)

    def test_expected_locations_with_specified_classes(self, input_dir,
                storage_dir, expected_icons_when_classes_specified, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder = classifier_data_set_builder.ClassifierDataSetBuilder(
            input_dir, storage_dir, classes=CLASSES
        )

        classifier_builder.split_and_build_data_sets()

        assert all(icon.exists() for icon in expected_icons_when_classes_specified)

    def test_info_file_content(self, classifier_builder, input_dir, expected_info, mocker):
        mocker.patch.object(
            classifier_data_set_builder.ClassifierDataSetBuilder,
            'split',
            return_value=SPLIT)

        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder.split_and_build_data_sets()

        assert all(info["info"] in info["file"].read_text() for info in expected_info)


def _create_icons(app_list, input_dir):
    for _, app in app_list.iterrows():
        icon_name = utils.get_app_icon_name(app["app_id"])
        (input_dir / icon_name).touch()
