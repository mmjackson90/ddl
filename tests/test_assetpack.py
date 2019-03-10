"""
Tests Assetpacks
"""

from ddl import AssetpackFactory, Assetpack
from ddl.asset import ComponentAsset


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


def test_change_assetpack_name():
    """Tests changing the name of an assetpack."""
    assetpack = AssetpackFactory.load('example_isometric')
    assetpack.change_assetpack_name('new_name')
    if len(assetpack.assets) != 7:
        raise AssertionError('%s != 7' % len(assetpack.assets))

    for key in assetpack.assets.keys():
        if key.split('.')[0] != 'new_name':
            raise AssertionError()

    for asset in assetpack.assets.values():
        if asset.assetpack_name != 'new_name':
            raise AssertionError()
        if isinstance(asset, ComponentAsset):
            for sub_part in asset.parts:
                if sub_part["asset_id"].split('.')[0] != 'new_name':
                    raise AssertionError()

    if assetpack.name != 'new_name':
        raise AssertionError()


def test_append_assetpacks():
    """
    Tests that appending one assetpack to another gives a bigger assetpack
    """
    assetpack = AssetpackFactory.load('example_isometric')
    assetpack2 = AssetpackFactory.load('example_isometric')
    assetpack2.change_assetpack_name('new_name')
    assetpack.append_assetpack(assetpack2)
    if len(assetpack.assets) != 14:
        raise AssertionError('%s != 14' % len(assetpack.assets))
