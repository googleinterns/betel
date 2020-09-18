import collections
from test import icon_builder as ib
import pytest
from betel import classifier_sequence


@pytest.fixture
def input_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("input_dir")


@pytest.fixture
def icon_builder(input_dir):
    return ib.IconBuilder(input_dir)


class TestClassifierSequence:
    @pytest.mark.parametrize("num_icons, expected_len", [
        (6, 2),  # 6 icons, batch size 3 => 2 batches
        (7, 3),  # 7 icons, batch size 3 => 3 batches
        (5, 2),  # 5 icons, batch size 3 => 2 batches
    ])
    def test_len(self, icon_builder, num_icons, expected_len):
        sequence = _get_sequence(icon_builder, num_icons=num_icons, batch_size=3)

        assert len(sequence) == expected_len

    def test_all_batches_have_full_batch_size(self, icon_builder):
        batches = []
        batch_size = 2
        sequence = _get_sequence(icon_builder, batch_size=batch_size, num_icons=3)

        for batch_x, batch_y in sequence:
            batches.append(batch_x)
            batches.append(batch_y)

        assert all([len(batch) == batch_size] for batch in batches)

    def test_all_icons_have_expected_size(self, icon_builder):
        sequence = _get_sequence(icon_builder, batch_size=1, num_icons=1)
        expected_icon_size = (1, 192, 192, 3)  # (batch_size, width, height, channels)

        assert sequence[0][0].shape == expected_icon_size

    @pytest.mark.parametrize("num_icons, expected_categories_sizes", [
        (10, {0: 3, 1: 3, 2: 4}),  # 10 icons, 3 categories => 3,3,4 icons/category
        (12, {0: 4, 1: 4, 2: 4}),  # 12 icons, 3 categories => 4,4,4 icons/category
    ])
    def test_categories_sizes(self, icon_builder, num_icons, expected_categories_sizes):
        sequence = _get_sequence(icon_builder, batch_size=5, num_icons=num_icons, num_categories=3)

        y_batches = []

        for _, batch_y in sequence:
            y_batches.extend(batch_y)

        y_batches = y_batches[:num_icons]

        counter = collections.Counter(y_batches)

        assert counter == expected_categories_sizes


def _get_sequence(icon_builder, batch_size, num_icons, num_categories=1):
    icon_builder.create_icons(num_icons=num_icons, num_categories=num_categories)

    sequence = classifier_sequence.ClassifierSequence(icon_builder.input_dir, batch_size, 192)
    return sequence
