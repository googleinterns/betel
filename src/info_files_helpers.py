import pathlib
from typing import Dict
import pandas as pd


def add_to_data(file: pathlib.Path, data: pd.DataFrame) -> None:
    """Adds data to file in CSV format.

    :param file: file to which data is added
    :param data: data to be added
    """
    with open(file, "a+") as csv_file:
        data.to_csv(csv_file, index=False, header=(file.stat().st_size == 0))


def part_of_data_set(file: pathlib.Path, data: Dict[str, str]) -> bool:
    """Checks if the data is already written in the CSV file.

    :param file: file to check
    :param data: data to be found (in dictionary format
    {column0: "value0", column1: "value1", ...})
    :return: if the data is already part of the data set
    """
    try:
        apps_details = pd.read_csv(file)
        return all([(apps_details[key] == data[key]).any() for key in data])
    except FileNotFoundError:
        return False


def read_list(file: pathlib.Path) -> pd.DataFrame:
    """Reads all the rows of a CSV file as a DataFrame

    :param file: file to read
    :return: a list of the CSV rows in DataFrame format
    """
    apps_details = pd.read_csv(file)
    return apps_details
