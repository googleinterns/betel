import pathlib
from typing import Tuple
from absl import app
from absl import flags
from betel.app_page_scraper import PlayAppPageScraper
from betel.info_files_helpers import read_csv_file
from betel.classifier_data_set_builder import ClassifierDataSetBuilder
from betel.classifier_sequence import ClassifierSequence
from betel.model_training import define_model, train_model

FLAGS = flags.FLAGS
PLAY_STORE_BASE_URL = "https://play.google.com/store/apps"

flags.DEFINE_bool('scrape', True, 'Do scraping.')
flags.DEFINE_bool('build', True, 'Build data set.')
flags.DEFINE_string('input_file', None, 'CSV file with app ids (scraper input).')
flags.DEFINE_string('scraper_storage_dir', './app_details', 'Directory for storing retrieved info.')
flags.DEFINE_list('category_filter', None, 'List of categories whose apps to keep.')
flags.DEFINE_string('builder_storage_dir', './data_set', 'Directory for split data sets.')
flags.DEFINE_list('classes', None, 'Classifier classes.')
flags.DEFINE_integer('batch_size', 32, 'Batch size.')
flags.DEFINE_integer('target_img_dim', 192, 'Image dimension(for square icons).')
flags.DEFINE_bool('shuffle', True, 'Shuffling after each epoch.')


def scrape_info() -> None:
    """Scrapes the necessary info from the Google Play Store."""
    scraper = PlayAppPageScraper(
        PLAY_STORE_BASE_URL,
        pathlib.Path(FLAGS.scraper_storage_dir),
        FLAGS.category_filter
    )

    app_ids = read_csv_file(
        pathlib.Path(FLAGS.input_file)).values.flatten()

    scraper.store_apps_info(app_ids)


def build_data_set() -> None:
    """"Splits the scraped data into train-validation-test data sets."""
    builder = ClassifierDataSetBuilder(
        pathlib.Path(FLAGS.scraper_storage_dir),
        pathlib.Path(FLAGS.builder_storage_dir),
        classes=FLAGS.classes
    )

    builder.split_and_build_data_sets()


def initialise_generators() -> Tuple:
    """Initialises generators for the train-validation-test data sets."""
    train_gen = ClassifierSequence(
        pathlib.Path(FLAGS.builder_storage_dir) / "train",
        FLAGS.batch_size,
        FLAGS.target_img_dim,
        FLAGS.shuffle
    )
    val_gen = ClassifierSequence(
        pathlib.Path(FLAGS.builder_storage_dir) / "validation",
        FLAGS.batch_size,
        FLAGS.target_img_dim,
        FLAGS.shuffle)
    test_gen = ClassifierSequence(
        pathlib.Path(FLAGS.builder_storage_dir) / "test",
        FLAGS.batch_size,
        FLAGS.target_img_dim,
        FLAGS.shuffle
    )

    return train_gen, val_gen, test_gen


def train() -> None:
    """Model training on the generated data sets."""
    model, backbone = define_model()

    train_gen, val_gen, _ = initialise_generators()

    train_model(model, backbone, train_gen, val_gen)


def main(argv):
    if FLAGS.scrape:
        scrape_info()

    if FLAGS.build:
        build_data_set()

    train()


if __name__ == "__main__":
    app.run(main)
