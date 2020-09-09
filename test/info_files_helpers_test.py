import pandas as pd
from src import add_to_data, part_of_data_set, read_list

DICTIONARIES = [{"a": "c", "b": "d"}, {"a": "e", "b": "f"}]
HEADER = "a,b"
ROWS = ["c,d", "e,f"]


class TestInfoFilesHelpers:
    def test_add_to_data(self, test_dir):
        file = test_dir / "info"

        data_frame = pd.DataFrame([DICTIONARIES[0]])
        add_to_data(file, data_frame)

        assert file.exists()
        assert HEADER in file.read_text()
        assert ROWS[0] in file.read_text()

    def test_part_of_data_set(self, test_dir):
        file = test_dir / "info"

        file.write_text(f"{HEADER}\n{ROWS[0]}")

        assert part_of_data_set(file, DICTIONARIES[0])
        assert not part_of_data_set(file, DICTIONARIES[1])

    def test_read_list(self, test_dir):
        file = test_dir / "info"

        file.write_text(f"{HEADER}\n{ROWS[0]}\n{ROWS[1]}")

        dict_list = read_list(file)

        assert dict_list.equals(pd.DataFrame(DICTIONARIES))
