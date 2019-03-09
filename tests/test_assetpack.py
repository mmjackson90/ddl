"""
Tests Assetpacks
"""

from ddl import AssetpackFactory, Assetpack


class FakeProjection:
    def __init__(self, width, height):
        self.width = width
        self.height = height


def test_factory_creates_assetpack():
    """ Ensure the AssetpackFactory returns an Assetpack. """
    assetpack = AssetpackFactory.load('example_isometric')
    assert isinstance(assetpack, Assetpack)


def test_assetpack_resize():
    """Test resizing an assetpack's images to match a new projection."""
    assetpack = AssetpackFactory.load('example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.resize_images(projection2)
    assert assetpack.projection.width == 29
    assert assetpack.projection.height == 17
    assert assetpack.images['floor-1x1-exact'].image.width == 29
    assert assetpack.images['floor-1x1-exact'].image.height == 19


def test_assetpack_resize():
    """Test rescaling an assetpack's components to match a new projection."""
    assetpack = AssetpackFactory.load('example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.rescale_components(projection2)
    assert assetpack.projection.width == 29
    assert assetpack.projection.height == 17
    assert assetpack.components['floor-2x2-exact'].parts[0]['x'] == 0
    assert assetpack.components['floor-2x2-exact'].parts[0]['y'] == 0
    assert assetpack.components['floor-2x2-exact'].parts[3]['x'] == 294/29
    assert assetpack.components['floor-2x2-exact'].parts[3]['y'] == 10
