import math
import collections
import pytest


class TestBetelClassifierSequence:
    def test_len(self, classifier_sequence, icons):
        assert len(classifier_sequence) == math.ceil(len(icons) / pytest.batch_size)

    def test_batch_size(self, classifier_sequence):
        batches = []

        for batch_x, batch_y in classifier_sequence:
            batches.append(batch_x)
            batches.append(batch_y)

        assert all([len(batch) == pytest.batch_size] for batch in batches)

    def test_image_size(self, classifier_sequence):
        incorrect_sized = []
        expected_size = (1,) + pytest.target_input_size + (3,)

        for batch_x, _ in classifier_sequence:
            for image in batch_x:
                if image.shape != expected_size:
                    incorrect_sized.append(image.name)

        assert not incorrect_sized

    def test_categories(self, classifier_sequence, icons):
        int_categories = [classifier_sequence.category_to_int[category]
                          for _, category in icons]
        expected_counter = collections.Counter(int_categories)

        y_batches = []

        for _, batch_y in classifier_sequence:
            y_batches.extend(batch_y)

        y_batches = y_batches[: len(icons)]

        counter = collections.Counter(y_batches)

        assert expected_counter == counter
