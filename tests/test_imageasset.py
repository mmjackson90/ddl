"""
Tests the methods of ImageAsset
"""

from ddl import ImageAsset
from PIL.PngImagePlugin import PngImageFile


def test_zero_top_left():
    """
    Tests an imageasset with no top left in the data
    initialises one at 0,0
    """
    data = {"name": "test_name",
            "id": "test",
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    if not image.assetpack_name == "example_isometric":
        raise AssertionError()
    if not image.name == "test_name":
        raise AssertionError()
    if not image.image_id == "test":
        raise AssertionError()
    if not isinstance(image.image, PngImageFile):
        raise AssertionError()
    if not image.top_left['x'] == 0:
        raise AssertionError()
    if not image.top_left['y'] == 0:
        raise AssertionError()


def test_nonzero_top_left():
    """Tests an imageasset with a top_left corectly sets itself"""
    data = {"name": "test_name",
            "id": "test",
            "top_left": {"x": 152, "y": 6},
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    if not image.assetpack_name == "example_isometric":
        raise AssertionError()
    if not image.name == "test_name":
        raise AssertionError()
    if not image.image_id == "test":
        raise AssertionError()
    if not isinstance(image.image, PngImageFile):
        raise AssertionError()
    if not image.top_left['x'] == 152:
        raise AssertionError()
    if not image.top_left['y'] == 6:
        raise AssertionError()


def test_resize():
    """Tests an image will resize the image and also move the top left"""
    data = {"name": "test_name",
            "id": "test",
            "top_left": {"x": 152, "y": 6},
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    image.resize(2, 3)
    if not image.image.width == 608:
        raise AssertionError()
    if not image.image.height == 603:
        raise AssertionError()
    if not image.top_left['x'] == 304:
        raise AssertionError()
    if not image.top_left['y'] == 18:
        raise AssertionError()
