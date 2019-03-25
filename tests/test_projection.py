"""
Tests Projections
"""

from ddl.projection import Projection, IsometricProjection, TopDownProjection


class FakeImageAsset:
    """A fake imageasset class"""
    def __init__(self):
        self.width = 1
        self.height = 1
        self.top_left = {'x': 2, 'y': 3}
        self.image_sizes = (10, 10)

    def resize(self, scale_1, scale_2):
        """ A fake resize function that just alters two internal parameters"""
        self.height = self.height*scale_1
        self.width = self.width*scale_2

    def get_image_sizes(self):
        """ A fake get size function that returns two known values"""
        return self.image_sizes


class FakeComponent:
    """A fake Component"""
    def __init__(self):
        self.scale_1 = 1
        self.scale_2 = 2

    def rescale(self, scale_1, scale_2):
        """ A fake resize function that just alters two internal parameters"""
        self.scale_1 = self.scale_1/scale_1
        self.scale_2 = self.scale_2/scale_2


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
    component = FakeComponent()
    components = {"test": component}
    projection1 = Projection(1, 1)
    projection2 = Projection(5, 5)
    projection1.rescale_components(components, projection2)
    if not component.scale_1 == 1/5:
        raise AssertionError()
    if not component.scale_2 == 2/5:
        raise AssertionError()


def test_get_image_pixel_list():
    """Goes through a list of images and grid co-ordinates and returns a
     list of images and pixel co-ordinates."""

    image = FakeImageAsset()
    projection1 = TopDownProjection(10, 10)
    image_location_list = [(image, 0, 0, False, False),
                           (image, 1, 2, False, False)]
    pixel_list = projection1.get_image_pixel_list(1, 3, image_location_list)
    # The image should not have been modified.
    assert pixel_list[0][0] == image
    assert pixel_list[0][1] == 8
    assert pixel_list[0][2] == 27
    assert pixel_list[1][0] == image
    assert pixel_list[1][1] == 18
    assert pixel_list[1][2] == 47


def test_flipped_td_pixel_list():
    """Goes through a list of images and grid co-ordinates and returns a
     list of images and pixel co-ordinates."""

    image = FakeImageAsset()
    projection1 = TopDownProjection(10, 10)
    image_location_list = [(image, 0, 0, True, False),
                           (image, 0, 0, False, True)]
    pixel_list = projection1.get_image_pixel_list(0, 0, image_location_list)
    # The image should not have been modified.
    assert pixel_list[0][0] == image
    assert pixel_list[0][1] == -8
    assert pixel_list[0][2] == -3
    assert pixel_list[1][0] == image
    assert pixel_list[1][1] == -2
    assert pixel_list[1][2] == -7


def test_flipped_iso_pixel_list():
    """Goes through a list of images and grid co-ordinates and returns a
     list of images and pixel co-ordinates."""

    image = FakeImageAsset()
    projection1 = IsometricProjection(10, 10)
    image_location_list = [(image, 0, 0, True, False),
                           (image, 0, 0, False, True)]
    pixel_list = projection1.get_image_pixel_list(0, 0, image_location_list)
    # The image should not have been modified.
    assert pixel_list[0][0] == image
    assert pixel_list[0][1] == -8
    assert pixel_list[0][2] == -3
    assert pixel_list[1][0] == image
    assert pixel_list[1][1] == -2
    assert pixel_list[1][2] == -7


def test_isometric_get_pixels():
    """Tests that the get_location_in_pixels function returns properly for
    the isometric case"""
    projection = IsometricProjection(16, 10)
    assert projection.get_location_in_pixels(0, 0) == (0, 0)
    assert projection.get_location_in_pixels(1, 0) == (8, 5)
    assert projection.get_location_in_pixels(1, 1) == (0, 10)
    assert projection.get_location_in_pixels(1, -1) == (16, 0)


def test_topdown_get_pixels():
    """Tests that the get_location_in_pixels function returns properly for
    the topdown case"""
    projection = TopDownProjection(16, 10)
    assert projection.get_location_in_pixels(0, 0) == (0, 0)
    assert projection.get_location_in_pixels(1, 0) == (16, 0)
    assert projection.get_location_in_pixels(1, 1) == (16, 10)
    assert projection.get_location_in_pixels(1, -1) == (16, -10)
