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

SPLIT = {'train': pd.DataFrame([{'app_id': 'com.play', 'category': 'play'},
                                {'app_id': 'com.page', 'category': 'page'},
                                {'app_id': 'com.example', 'category': 'example'}]),
         'validation': pd.DataFrame([{'app_id': 'com.test', 'category': 'example'}]),
         'test': pd.DataFrame([{'app_id': 'com.store', 'category': 'store'}])}

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
        storage_dir / "train" / "play" / "icon_com.play",
        storage_dir / "validation" / "example" / "icon_com.test",
        storage_dir / "test" / "store" / "icon_com.store"
    ]


@pytest.fixture
def expected_icons_when_classes_specified(storage_dir):
    return [
        storage_dir / "train" / "example" / "icon_com.example",
        storage_dir / "train" / "others" / "icon_com.page",
        storage_dir / "train" / "play" / "icon_com.play",
        storage_dir / "validation" / "example" / "icon_com.test",
        storage_dir / "test" / "others" / "icon_com.store"
    ]


@pytest.fixture
def expected_info(storage_dir):
    return [
        {"file": storage_dir / "info" / "example", "info": "com.example,train"},
        {"file": storage_dir / "info" / "page", "info": "com.page,train"},
        {"file": storage_dir / "info" / "store", "info": "com.store,test"},
        {"file": storage_dir / "info" / "play", "info": "com.play,train"},
        {"file": storage_dir / "info" / "example", "info": "com.test,validation"}
    ]


class TestClassifierDataSetBuilder:
    def test_split(self, classifier_builder):
        split = classifier_builder.split(APP_LIST)

        for data_set in split:
            assert((split[data_set].values == split[data_set].values).all())

    def test_expected_locations(self, classifier_builder, input_dir, expected_icons):
        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder.split_and_build_data_sets()

        for icon in expected_icons:
            assert icon.exists()

    def test_expected_locations_with_specified_classes(self, input_dir,
                storage_dir, expected_icons_when_classes_specified):
        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder = classifier_data_set_builder.ClassifierDataSetBuilder(
            input_dir, storage_dir, classes=CLASSES
        )

        classifier_builder.split_and_build_data_sets()

        for icon in expected_icons_when_classes_specified:
            assert icon.exists()

    def test_info_file_content(self, classifier_builder, input_dir, expected_info):
        input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME
        input_file.write_text(CSV)

        _create_icons(APP_LIST, input_dir)

        classifier_builder.split_and_build_data_sets()

        for info in expected_info:
            assert info["info"] in info["file"].read_text()


def _create_icons(app_list, input_dir):
    for _, app in app_list.iterrows():
        icon_name = utils.get_app_icon_name(app["app_id"])
        (input_dir / icon_name).touch()
