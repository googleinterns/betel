import pytest
import pandas as pd
from betel import info_files_helpers

DICTIONARIES = [{"a": "c", "b": "d"}, {"a": "e", "b": "f"}]
HEADER = "a,b"
ROWS = ["c,d", "e,f"]


@pytest.fixture
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_dir")


class TestInfoFilesHelpers:
    def test_add_to_data(self, test_dir):
        file = test_dir / "info"

        data_frame = pd.DataFrame([DICTIONARIES[0]])
        info_files_helpers.add_to_data(file, data_frame)

        assert file.exists()
        assert HEADER in file.read_text()
        assert ROWS[0] in file.read_text()

    def test_part_of_data_set(self, test_dir):
        file = test_dir / "info"

        file.write_text(f"{HEADER}\n{ROWS[0]}")

        present_data_frame = pd.DataFrame([DICTIONARIES[0]])
        missing_data_frame = pd.DataFrame([DICTIONARIES[1]])

        assert info_files_helpers.part_of_data_set(file, present_data_frame)
        assert not info_files_helpers.part_of_data_set(file, missing_data_frame)

    def test_read_list(self, test_dir):
        file = test_dir / "info"

        file.write_text(f"{HEADER}\n{ROWS[0]}\n{ROWS[1]}")

        content = info_files_helpers.read_csv_file(file)

        assert content.equals(pd.DataFrame(DICTIONARIES))
