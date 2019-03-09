"""
Tests Projections
"""

from ddl.projection import Projection, IsometricProjection, TopDownProjection
# TODO: Mock the fuck out of these
from ddl import ImageAsset, Component


class FakeImageAsset:
    """A fake imageasset class"""
    def __init__(self):
        self.width = 1
        self.height = 1

    def resize(self, x, y):
        self.height = self.height*x
        self.width = self.width*y


def test_get_grid_ratios():
    """ Tests a projection returns the correct ratios"""
    projection1 = Projection(10, 10)
    projection2 = Projection(20, 30)
    if not projection1.get_grid_ratios(projection2) == (2, 3):
        raise AssertionError()


def test_alter_grid_parameters():
    """ Tests a projection returns the correct ratios"""
    projection1 = Projection(10, 10)
    projection2 = Projection(20, 30)
    projection1.alter_grid_parameters(projection2)
    if not projection1.width == 20:
        raise AssertionError()
    if not projection1.height == 30:
        raise AssertionError()


def test_resize_images():
    """Tests that a list of images resizes correctly"""
    image = FakeImageAsset()
    images = {"test": image}
    projection1 = Projection(2, 2)
    projection2 = Projection(5, 10)
    projection1.resize_images(images, projection2)
    image.width = 2/5
    image.height = 5


def test_rescale_components():
    """Tests that a list of components rescales correctly"""
    data = {
        "name": "2x2 Floor exact",
        "id": "floor-2x2-exact",
        "parts": [
            {
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 0,
                "y": 0
            },
            {
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 1,
                "y": 2
            }
        ],
        "tags": [
            "example"
        ]
    }

    component = Component(data, "example_isometric")
    components = {"test": component}
    projection1 = Projection(1, 1)
    projection2 = Projection(5, 5)
    projection1.rescale_components(components, projection2)
    if not component.data["parts"][0]["x"] == 0:
        raise AssertionError()
    if not component.data["parts"][0]["y"] == 0:
        raise AssertionError()
    if not component.data["parts"][1]["x"] == 1/5:
        raise AssertionError()
    if not component.data["parts"][1]["y"] == 2/5:
        raise AssertionError()


def test_get_image_pixel_list():
    """Goes through a list of images and grid co-ordinates and returns a
     list of images and pixel co-ordinates."""
    image_data = {"name": "test",
                  "id": "test",
                  "top_left": {"x": 152, "y": 6},
                  "image": "1x1_floor_fuzzy.png"}
    image = ImageAsset(image_data, "example_isometric")
    projection1 = TopDownProjection(10, 10)
    image_location_list = [(image, 0, 0), (image, 1, 2)]
    pixel_list = projection1.get_image_pixel_list(1, 3, image_location_list)
    if not isinstance(pixel_list[0][0], ImageAsset):
        raise AssertionError()
    if not pixel_list[0][1] == 10:
        raise AssertionError()
    if not pixel_list[0][2] == 30:
        raise AssertionError()
    if not isinstance(pixel_list[1][0], ImageAsset):
        raise AssertionError()
    if not pixel_list[1][1] == 20:
        raise AssertionError()
    if not pixel_list[1][2] == 50:
        raise AssertionError()


def test_isometric_get_pixels():
    """Tests that the get_location_in_pixels function returns properly for
    the isometric case"""
    projection = IsometricProjection(16, 10)
    if not projection.get_location_in_pixels(0, 0) == (0, 0):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, 0) == (-8, 5):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, 1) == (0, 10):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, -1) == (-16, 0):
        raise AssertionError()


def test_topdown_get_pixels():
    """Tests that the get_location_in_pixels function returns properly for
    the topdown case"""
    projection = TopDownProjection(16, 10)
    if not projection.get_location_in_pixels(0, 0) == (0, 0):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, 0) == (16, 0):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, 1) == (16, 10):
        raise AssertionError()
    if not projection.get_location_in_pixels(1, -1) == (16, -10):
        raise AssertionError()
