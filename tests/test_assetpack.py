"""
Tests Assetpacks
"""

import os

from ddl.assetpack import AssetpackFactory, Assetpack
from ddl.asset import ComponentAsset


class FakeProjection:
    """ A fake projection class to spoof width and height parameters only."""
    def __init__(self, width, height):
        self.width = width
        self.height = height


def test_factory_creates_assetpack():
    """ Ensure the AssetpackFactory returns an Assetpack. """
    pack_path = os.path.abspath('assetpacks/example_isometric')
    assetpack = AssetpackFactory.load(pack_path)
    if not isinstance(assetpack, Assetpack):
        raise AssertionError()


def test_assetpack_resize():
    """Test resizing an assetpack's images to match a new projection."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.resize_images(projection2)
    if not assetpack.projection.width == 29:
        raise AssertionError()
    if not assetpack.projection.height == 17:
        raise AssertionError()
    if not assetpack.images['example_isometric.floor-1x1-exact'
                            ].image.width == 29:
        raise AssertionError()
    if not assetpack.images['example_isometric.floor-1x1-exact'
                            ].image.height == 19:
        raise AssertionError()


def test_assetpack_rescale():
    """Test rescaling an assetpack's components to match a new projection."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    projection2 = FakeProjection(29, 17)
    assetpack.rescale_components(projection2)
    if not assetpack.projection.width == 29:
        raise AssertionError()
    if not assetpack.projection.height == 17:
        raise AssertionError()
    if not assetpack.components['example_isometric.floor-2x2-exact'
                                ].parts[0]['x'] == 0:
        raise AssertionError()
    if not assetpack.components['example_isometric.floor-2x2-exact'
                                ].parts[0]['y'] == 0:
        raise AssertionError()
    if not assetpack.components['example_isometric.floor-2x2-exact'
                                ].parts[3]['x'] == 294/29:
        raise AssertionError()
    if not assetpack.components['example_isometric.floor-2x2-exact'
                                ].parts[3]['y'] == 10:
        raise AssertionError()


def test_change_assetpack_name():
    """Tests changing the name of an assetpack."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    assetpack.change_assetpack_id('new_name')
    if len(assetpack.images) != 4:
        raise AssertionError()
    if len(assetpack.components) != 4:
        raise AssertionError()

    for key in assetpack.images.keys():
        if key.split('.')[0] != 'new_name':
            raise AssertionError()

    for key in assetpack.components.keys():
        if key.split('.')[0] != 'new_name':
            raise AssertionError()

    for component in assetpack.components.values():
        if component.assetpack_id != 'new_name':
            raise AssertionError()
        if isinstance(component, ComponentAsset):
            for sub_part in component.parts:
                if sub_part["asset_id"].split('.')[0] != 'new_name':
                    raise AssertionError()

    if assetpack.pack_id != 'new_name':
        raise AssertionError()


def test_append_assetpacks():
    """
    Tests that appending one assetpack to another gives a bigger assetpack
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    assetpack2 = AssetpackFactory.load('assetpacks/example_isometric')
    assetpack2.change_assetpack_id('new_name')
    assetpack.append_assetpack(assetpack2)
    if len(assetpack.images) != 8:
        raise AssertionError('%s != 14' % len(assetpack.images))
    if len(assetpack.components) != 8:
        raise AssertionError()


def test_simple_image_location_list():
    """Tests an assetpack will return an imagelocationlist for a simple
    component if asked. No Nesting."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component = assetpack.components['example_isometric.floor-wall-exact']
    ill = assetpack.get_image_location_list(2, 3, component)
    if len(ill) != 2:
        raise AssertionError()
    # Required to check things are ending up in the right places in the list
    if not ill[0][0].asset_id == "floor-1x1-exact":
        raise AssertionError(ill[0][0].asset_id)
    if not ill[1][0].asset_id == "exact-wall-1":
        raise AssertionError()


def test_nested_image_location_list():
    """Tests an assetpack will return an imagelocationlist for a complex
    component if asked. Nesting involved."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component = assetpack.components['example_isometric.nested-component-test']
    ill = assetpack.get_image_location_list(2, 3, component)
    if len(ill) != 3:
        raise AssertionError()
    # Required to check things are ending up in the right places in the list
    if not ill[0][0].asset_id == "floor-1x1-exact":
        raise AssertionError(ill[0][0].asset_id)
    if not ill[1][0].asset_id == "exact-wall-1":
        raise AssertionError()
    if not ill[2][0].asset_id == "floor-1x1-fuzzy":
        raise AssertionError()
    # Required to check recursive offsets are being correctly propagated
    if not ill[0][1] == 2:
        raise AssertionError(ill[0][2])
    if not ill[0][2] == 3:
        raise AssertionError()
    if not ill[2][1] == 5:
        raise AssertionError()
    if not ill[2][2] == 4:
        raise AssertionError()
