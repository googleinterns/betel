from pathlib import Path
from typing import Dict, List
from csv import DictWriter, DictReader


def add_to_data(file: Path, data: Dict[str, str]) -> None:
    """Adds (dictionary) data to file in CSV format.

    :param file: file to which data is added
    :param data: data to be added in (dictionary format
    {column0: "value0", column1: "value1", ...})
    """
    fieldnames = list(data)

    with open(file, "a+") as output_file:
        dict_writer = DictWriter(output_file, fieldnames=fieldnames)
        if file.stat().st_size == 0:
            dict_writer.writeheader()
        dict_writer.writerow(data)


def part_of_data_set(file: Path, data: Dict[str, str]) -> bool:
    """Checks if the data is already written in the CSV file.

    :param file: file to check
    :param data: data to be found (in dictionary format
    {column0: "value0", column1: "value1", ...})
    :return: if the data is already part of the data set
    """
    fields_to_compare = list(data)

    try:
        with open(file, "r") as info_file:
            dict_reader = DictReader(info_file)
            for row in dict_reader:
                if all(data[field] == row[field] for field in fields_to_compare):
                    return True
            return False
    except FileNotFoundError:
        return False


def read_list(file: Path) -> List[Dict[str, str]]:
    """Reads all the rows of a CSV file as a dictionary
     ({column0: "value0", column1: "value1", ...}) and
    returns a list containing them.

    :param file: file to read
    :return: a list of the CSV rows in Dict format
    """
    with open(file, "r") as input_file:
        dict_reader = DictReader(input_file)
        apps_details = list(dict_reader)
    return apps_details


def log_failure(file: Path, message: str, exception: Exception) -> None:
    """Logs an exception in the specified file.

    :param file: log file
    :param message: info about the exception
    :param exception: the caught exception
    """
    with open(file, "a+") as log_file:
        info = f"{message}, {getattr(exception, 'message', repr(exception))}\n"
        log_file.write(info)
