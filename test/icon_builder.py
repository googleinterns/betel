import pathlib
from PIL import Image


class IconBuilder:
    """A factory class for creating test app icons."""

    input_dir: pathlib.Path

    def __init__(self, input_dir: pathlib.Path, image_size: (int, int) = (180, 180)):
        self._image_size = image_size
        self.input_dir = input_dir

    def create_icons(self, num_icons: int, num_categories: int = 1):
        """ Creates num_icons icons equally distributed in num_categories
        categories (the last category has more icons in case of inexact
        division.

        :param num_icons: number of icons to be created
        :param num_categories: number of categories in which to
        equally distribute the icons
        """
        icons_no = [num_icons // num_categories] * num_categories
        icons_no[num_categories - 1] += num_icons % num_categories
        for category_index in range(num_categories):
            category_dir = self.input_dir / f"category{category_index}"
            category_dir.mkdir()

            for icon_index in range(icons_no[category_index]):
                icon = category_dir / f"icon_{category_index}.{icon_index}"
                icon.touch()
                image = Image.new('RGBA', size=self._image_size)
                image.save(icon, 'png')
