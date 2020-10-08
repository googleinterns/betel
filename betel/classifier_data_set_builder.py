import shutil
import pathlib
import pandas as pd
from betel import utils
from betel import info_files_helpers
from betel import data_set_builder


class ClassifierDataSetBuilder(data_set_builder.DataSetBuilder):
    """A class for splitting classifier data into train-validation-test sets."""

    def __init__(self, input_dir: pathlib.Path, storage_dir: pathlib.Path,
                 split_ratio: (float, float, float) = (0.7, 0.15, 0.15),
                 classes: [str] = None):
        """Constructor.

        :param input_dir: data to be split (output of the scraper,
        meaning a directory containing the input icons and a csv file
        describing the whole data set)
        :param storage_dir: storage directory for split data sets
        :param split_ratio: the ratio for train-validation-test data sets
        :param classes: the classes desired for the classifier (should be
        Google Play Store categories)
        """
        super().__init__(input_dir, storage_dir, split_ratio)

        # directory to store the info about the split
        self._info_dir = storage_dir / utils.CLASSIFIER_DATA_BUILDER_INFO_DIR
        self._info_dir.mkdir(exist_ok=True)

        self._classes = classes

    def _sort(self, app_list: pd.DataFrame) -> pd.DataFrame:
        return app_list.sort_values(by=["app_id"])

    def _add_to_data_set(self, element: pd.Series, data_set: str) -> None:
        app_id = element["app_id"]
        category = element["category"]

        if self._classes is not None:
            category = category if category in self._classes else "others"

        info_file = self._info_dir / category
        icon_name = utils.get_app_icon_name(app_id)
        app_icon = self._input_dir / icon_name

        search_data_frame = utils.get_app_search_data_frame(app_id)
        part_of_data = (
            info_files_helpers.part_of_data_set(info_file, search_data_frame)
        )

        if not part_of_data and app_icon.exists():
            app_info = _build_app_info_data_frame(app_id, data_set)
            info_files_helpers.add_to_data(info_file, app_info)

            directory = self._storage_dir / data_set / category
            _add_icon_to_data_set(app_icon, icon_name, directory)


def _build_app_info_data_frame(app_id: str, data_set: str) -> pd.DataFrame:
    dictionary = {"app_id": app_id, "data_set": data_set}
    return pd.DataFrame([dictionary])


def _add_icon_to_data_set(app_icon: pathlib.Path, icon_name: str, directory: pathlib.Path) -> None:
    directory.mkdir(exist_ok=True, parents=True)
    shutil.copy(app_icon, directory / icon_name)
