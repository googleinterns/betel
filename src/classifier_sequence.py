import pathlib
import sys
import math
from typing import Callable
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageOps


class BetelClassifierSequence(keras.utils.Sequence):
    """A class for sequencing the classifier's input data."""

    def __init__(self, input_dir: pathlib.Path, batch_size: int,
                 preprocess_func: Callable = keras.applications.mobilenet_v2.preprocess_input,
                 target_input_size: (int, int) = (192, 192)):
        """Constructor.

        :param input_dir: directory with input data
        :param batch_size: the desired size of a batch
        :param preprocess_func: preprocessing function specific to a model
        :param target_input_size: target input size for the classifier
        """
        if not input_dir.exists():
            print("Invalid input directory.")
            sys.exit()

        self._input_dir = input_dir
        self._batch_size = batch_size
        self._app_icons = []

        categories = []
        for category in self._input_dir.iterdir():
            categories.append(category.name)
            icons = [(icon.name, category.name) for icon in category.iterdir()]
            self._app_icons.extend(icons)

        self.int_to_category = dict(enumerate(categories))
        self.category_to_int = {y: x for x, y in enumerate(categories)}

        self._target_input_size = target_input_size
        self._preprocess_func = preprocess_func

    def __len__(self):
        return math.ceil(len(self._app_icons) / self._batch_size)

    def __getitem__(self, idx):
        batch_app_icons = self._app_icons[idx * self._batch_size : (idx + 1) * self._batch_size]

        batch_app_icons = self._fit_to_batch_size(batch_app_icons)

        batch_x = []
        batch_y = []

        for app_info in batch_app_icons:
            icon_name, category = app_info

            icon = self._input_dir / category / icon_name
            img = Image.open(icon)

            resized_icon = self._resize_input(img)

            icon = keras.preprocessing.image.img_to_array(resized_icon)
            icon = icon[:, :, :3]  # discarding the alpha channel
            icon = self._preprocess_func(icon[tf.newaxis, ...])

            batch_x.append(icon)
            batch_y.append(self.category_to_int[category])

        return np.array(batch_x), np.array(batch_y)

    def _fit_to_batch_size(self, batch: []) -> []:
        while self._batch_size != len(batch):
            size_difference = self._batch_size - len(batch)
            batch.extend(batch[:size_difference])
        return batch

    def _resize_input(self, img: Image) -> Image:
        border = tuple(np.floor_divide(np.subtract(self._target_input_size, img.size), 2))

        if all(size > 0 for size in border):
            resized_icon = ImageOps.expand(img, border=border, fill="black")
        else:
            resized_icon = img.crop((-border[0],
                                     -border[1],
                                     -border[0] + self._target_input_size[0],
                                     -border[1] + self._target_input_size[1]))
        return resized_icon
