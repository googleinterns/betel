import pathlib
import pandas as pd


def add_to_data(file: pathlib.Path, data: pd.DataFrame) -> None:
    """Adds data to file in CSV format.

    :param file: file to which data is added
    :param data: data to be added
    """
    with open(file, "a+") as csv_file:
        data.to_csv(csv_file, index=False, header=(file.stat().st_size == 0))


def part_of_data_set(file: pathlib.Path, data: pd.DataFrame) -> bool:
    """Checks if the data is already written in the CSV file.

    :param file: file to check
    :param data: DataFrame to be found
    :return: if the data is already part of the data set
    """
    try:
        apps_details = pd.read_csv(file)
        for key in data.columns:
            if not (apps_details[key].values == data[key].values).any():
                return False
        return True
    except FileNotFoundError:
        return False


def read_csv_file(file: pathlib.Path) -> pd.DataFrame:
    """Reads all the rows of a CSV file as a DataFrame.

    :param file: file to read
    :return: a list of the CSV rows in DataFrame format
    """
    apps_details = pd.read_csv(file)
    return apps_details
