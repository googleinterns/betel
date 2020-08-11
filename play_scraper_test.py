import numpy as np
from play_scraper import PlayPageScraper


def test_get_icon(directory, subdir):
    test_dir = "test_data/"
    rand_array = np.random.randint(0, 255, 10)
    file_name = "icon_com.example"
    np.savetxt(test_dir + file_name, rand_array, fmt="%d")

    play_scraper = PlayPageScraper("file:./" + test_dir, directory)
    play_scraper.get_icon("com.example", directory=subdir)

    read_array = np.loadtxt(directory + subdir + file_name, dtype=int)
    assert np.array_equal(rand_array, read_array)
