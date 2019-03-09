"""
Tests the methods of ImageAsset
"""

from ddl import ImageAsset
from PIL.PngImagePlugin import PngImageFile


def test_zero_top_left_initialisation():
    """
    Tests an imageasset with no top left in the data
    initialises one at 0,0
    """
    data = {"name": "test_name",
            "id": "test",
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    assert image.assetpack_name == "example_isometric"
    assert image.name == "test_name"
    assert image.image_id == "test"
    assert isinstance(image.image, PngImageFile)
    assert image.top_left['x'] == 0
    assert image.top_left['y'] == 0


def test_nonzero_top_left_initialisation():
    """Tests an imageasset with a top_left corectly sets itself"""
    data = {"name": "test_name",
            "id": "test",
            "top_left": {"x": 152, "y": 6},
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    assert image.assetpack_name == "example_isometric"
    assert image.name == "test_name"
    assert image.image_id == "test"
    assert isinstance(image.image, PngImageFile)
    assert image.top_left['x'] == 152
    assert image.top_left['y'] == 6


def test_resize():
    """Tests an image will resize the image and also move the top left"""
    data = {"name": "test_name",
            "id": "test",
            "top_left": {"x": 152, "y": 6},
            "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(data, "example_isometric")
    image.resize(2, 3)
    assert image.image.width == 608
    assert image.image.height == 603
    assert image.top_left['x'] == 304
    assert image.top_left['y'] == 18
