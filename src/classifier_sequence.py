import pathlib
import math
import numpy as np
from typing import Dict, Tuple, List
from tensorflow import keras
from PIL import Image, ImageOps


class ClassifierSequence(keras.utils.Sequence):
    """A class for sequencing the classifier's input data."""

    category_id_to_name: Dict[int, str]
    category_name_to_id: Dict[str, int]

    def __init__(self, input_dir: pathlib.Path, batch_size: int,
                 target_img_dim: int, shuffle: bool = True):
        """Constructor.

        :param input_dir: directory with input data
        :param batch_size: the desired size of a batch
        :param target_img_dim: target dimension (for square icons)
        :param shuffle: whether the input data is shuffled on epoch end or not.
        """
        if not input_dir.exists():
            raise ValueError("Input directory does not exist.")

        self._input_dir = input_dir
        self._batch_size = batch_size
        self._app_icons = []
        self._shuffle = shuffle
        self._target_icon_size = (target_img_dim, target_img_dim)

        categories = self._get_categories()

        self.category_id_to_name = dict(enumerate(categories))
        self.category_name_to_id = {y: x for x, y in enumerate(categories)}

    def __len__(self) -> int:
        return math.ceil(len(self._app_icons) / self._batch_size)

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        batch_app_icons = self._app_icons[idx * self._batch_size: (idx + 1) * self._batch_size]

        batch_app_icons = self._fit_to_batch_size(batch_app_icons)

        batch_x = []
        batch_y = []

        for icon_name, category in batch_app_icons:
            icon = self._load_icon(icon_name, category)

            batch_x.append(icon)
            batch_y.append(self.category_name_to_id[category])

        return np.array(batch_x), np.array(batch_y)

    def on_epoch_end(self) -> None:
        """Shuffle data after each epoch."""
        if self._shuffle:
            np.random.shuffle(self._app_icons)

    def _load_icon(self, icon_name: str, category: str) -> np.ndarray:
        icon = self._input_dir / category / icon_name
        img = keras.preprocessing.image.load_img(icon)

        resized_icon = self._resize_input(img)

        icon = keras.preprocessing.image.img_to_array(resized_icon)
        icon = icon[:, :, :3]  # discarding the alpha channel

        return icon

    def _get_categories(self) -> List[str]:
        categories = []
        for category in self._input_dir.iterdir():
            categories.append(category.name)
            self._add_icons(category)
        return categories

    def _add_icons(self, category: pathlib.Path) -> None:
        icons = [(icon.name, category.name) for icon in category.iterdir()]
        self._app_icons.extend(icons)

    def _fit_to_batch_size(self, batch: List) -> List:
        while self._batch_size != len(batch):
            missing_items_no = self._batch_size - len(batch)
            batch.extend(self._app_icons[:missing_items_no])
        return batch

    def _resize_input(self, img: Image) -> Image:
        border = tuple(np.floor_divide(np.subtract(self._target_icon_size, img.size), 2))

        if all(size > 0 for size in border):
            resized_icon = ImageOps.expand(img, border=border, fill="black")
        else:
            resized_icon = img.crop((-border[0],
                                     -border[1],
                                     -border[0] + self._target_icon_size[0],
                                     -border[1] + self._target_icon_size[1]))
        return resized_icon
