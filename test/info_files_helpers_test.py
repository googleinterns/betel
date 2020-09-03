from src import add_to_data, part_of_data_set, read_list, log_failure, BetelError

DICTIONARIES = [{"a": "c", "b": "d"}, {"a": "e", "b": "f"}]
HEADER = "a,b"
ROWS = ["c,d", "e,f"]


class TestInfoFilesHelpers:
    def test_add_to_data(self, test_dir):
        file = test_dir / "info"

        add_to_data(file, DICTIONARIES[0])

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

        assert dict_list == DICTIONARIES

    def test_log_failure(self, icon_dir):
        app_id = "app_id"
        exception = BetelError("This is an error.")
        expected_text = f"{app_id}, {getattr(exception, 'message', repr(exception))}\n"
        log_file = icon_dir / "logs"

        log_failure(log_file, app_id, exception)

        assert log_file.read_text() == expected_text
