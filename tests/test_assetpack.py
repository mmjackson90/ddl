"""
Tests Assetpacks
"""

from ddl import AssetpackFactory, Assetpack


class FakeProjection:
    """ A fake projection class to spoof width and height parameters only."""
    def __init__(self, width, height):
        self.width = width
        self.height = height


def test_factory_creates_assetpack():
    """ Ensure the AssetpackFactory returns an Assetpack. """
    assetpack = AssetpackFactory.load('example_isometric')
    if not isinstance(assetpack, Assetpack):
        raise AssertionError()


def test_assetpack_resize():
    """Test resizing an assetpack's images to match a new projection."""
    assetpack = AssetpackFactory.load('example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.resize_images(projection2)
    if not assetpack.projection.width == 29:
        raise AssertionError()
    if not assetpack.projection.height == 17:
        raise AssertionError()
    if not assetpack.assets['example_isometric.i.floor-1x1-exact'
                            ].image.width == 29:
        raise AssertionError()
    if not assetpack.assets['example_isometric.i.floor-1x1-exact'
                            ].image.height == 19:
        raise AssertionError()


def test_assetpack_rescale():
    """Test rescaling an assetpack's components to match a new projection."""
    assetpack = AssetpackFactory.load('example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.rescale_components(projection2)
    if not assetpack.projection.width == 29:
        raise AssertionError()
    if not assetpack.projection.height == 17:
        raise AssertionError()
    if not assetpack.assets['example_isometric.c.floor-2x2-exact'
                            ].parts[0]['x'] == 0:
        raise AssertionError()
    if not assetpack.assets['example_isometric.c.floor-2x2-exact'
                            ].parts[0]['y'] == 0:
        raise AssertionError()
    if not assetpack.assets['example_isometric.c.floor-2x2-exact'
                            ].parts[3]['x'] == 294/29:
        raise AssertionError()
    if not assetpack.assets['example_isometric.c.floor-2x2-exact'
                            ].parts[3]['y'] == 10:
        raise AssertionError()
