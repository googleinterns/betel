import pathlib
import abc
from typing import Dict
import pandas as pd
from betel import utils
from betel import info_files_helpers


class DataSetBuilder(metaclass=abc.ABCMeta):
    """A class for splitting data into train-validation-test sets."""

    _RANDOM_SEED = 2579  # seed for random splitting

    def __init__(self, input_dir: pathlib.Path, storage_dir: pathlib.Path):
        """"Constructor.

        :param input_dir: data to be split (output of the scraper)
        :param storage_dir: storage directory for split data sets
        """
        self._storage_dir = storage_dir
        self._storage_dir.mkdir(exist_ok=True, parents=True)

        self._input_dir = input_dir
        self._input_file = input_dir / utils.SCRAPER_INFO_FILE_NAME

    def split(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Randomly splits a list of data into 3
        (train-validation-test).

        :param data: the list to be split
        :return: the train-validation-test split in Dict format
        """
        app_list = self._sort(data)
        app_list = app_list.sample(frac=1, random_state=self._RANDOM_SEED)

        index_1 = int(0.7 * len(app_list))
        index_2 = int(0.85 * len(app_list))
        train = app_list.iloc[:index_1]
        validation = app_list.iloc[index_1:index_2]
        test = app_list.iloc[index_2:]

        split = {
            "train": train,
            "validation": validation,
            "test": test
        }

        return split

    def split_and_build_data_sets(self) -> None:
        """Splits and builds the train-validation-test data sets."""
        app_list = info_files_helpers.read_csv_file(self._input_file)

        split = self.split(app_list)

        for data_set in split:
            self._build_set(data_set, split[data_set])

    def _build_set(self, data_set: str, elements: pd.DataFrame) -> None:
        for _, row in elements.iterrows():
            self._add_to_data_set(row, data_set)

    @abc.abstractmethod
    def _sort(self, app_list: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_to_data_set(self, element: pd.Series, data_set: str) -> None:
        raise NotImplementedError
