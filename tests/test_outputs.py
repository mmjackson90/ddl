"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl.assetpack import AssetpackFactory
from ddl.renderer import Renderer
from ddl.asset import ComponentAsset
import hashlib

import os


def setup_module(module):
    """Makes sure there's somewhere to dump the output tests"""
    if not os.path.exists('tests/test_outputs/'):
        os.makedirs('tests/test_outputs/')


def test_smoke_render_component():
    """
    Smoke test loading and rendering a component with multiple
    images that came from a definition.
    """

    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-2x2-exact']
    image_location_list = floor1.get_image_location_list(0, 0)

    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('file', filepath='tests/test_outputs/floor1_iso.png')
    with open("tests/test_outputs/floor1_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '0ea8c817569bf0deb7cfcd9978811af3'


def test_smoke_design_component():
    """
    Smoke test creating a new component and then passing it to a renderer.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    data = {
        "name": '',
        "id": 'floor-1x2-exact',
        "parts": [],
        "tags": []
    }
    floor4 = ComponentAsset(data, assetpack)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 0, 0)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 0, 1)

    image_location_list2 = floor4.get_image_location_list(0, 0)
    image_pixel_list2 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list2)
    renderer2 = Renderer(image_pixel_list=image_pixel_list2)
    renderer2.output('file', filepath='tests/test_outputs/floor4_iso.png')
    with open("tests/test_outputs/floor4_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == 'a71791bf3289dccebb16e0935e29d484'


def test_smoke_twiddly():
    """
    Smoke test creating a new component, removing a bit, and then using the
    component factory's built in output method to render it, before testing the
    clear component functionality and finally rendering out some fuzzy tiles.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    data = {
        "name": '',
        "id": 'twiddle_1',
        "parts": [],
        "tags": []
    }
    floor4 = ComponentAsset(data, assetpack)
    floor4.add_component(assetpack.components["easy-dungeon-ddl-example-iso.floor-2x2-exact"], 0, 0)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 2, 1)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 2, 2)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 2, 3)
    floor4.add_component(assetpack.components["easy-dungeon-ddl-example-iso.floor-2x2-exact"], 3, 3)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-fuzzy"], 4, 4)
    floor4.remove_last_part()
    renderer4_1 = Renderer(image_pixel_list=assetpack.projection.
                           get_image_pixel_list(0, 0, floor4.get_image_location_list(0, 0)))
    renderer4_1.output('file', filepath='tests/test_outputs/twiddly_iso.png')
    with open("tests/test_outputs/twiddly_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '438b0ce4465c7626179d394efb3a6126'


def test_smoke_fuzzy():
    """
    Smoke test creating a new component, removing a bit, and then using the
    component factory's built in output method to render it, before testing the
    clear component functionality and finally rendering out some fuzzy tiles.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    data = {
        "name": '',
        "id": 'fuzzy',
        "parts": [],
        "tags": []
    }
    fuzzy = ComponentAsset(data, assetpack)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 0, 0)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-fuzzy"], 0, 1)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-fuzzy"], 1, 0)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 1, 1)

    renderer4_2 = Renderer(image_pixel_list=assetpack.projection.
                           get_image_pixel_list(0, 0, fuzzy.get_image_location_list(0, 0)))
    renderer4_2.output('file', filepath='tests/test_outputs/fuzzy_iso.png')
    with open("tests/test_outputs/fuzzy_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '26805851de99484aba096fdd8e76cf43'


def test_smoke_wall():
    """
    Smoke test a wall/floor combo, just to check the offsets look good.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor_wall = assetpack.components['easy-dungeon-ddl-example-iso.double-floor-wall-exact']
    ill = floor_wall.get_image_location_list(0, 0)
    renderer5 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, ill))

    renderer5.output('file', filepath='tests/test_outputs/wall_iso.png')
    with open("tests/test_outputs/wall_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '7b85b07e0b7a28439c98618db60ae360'


def test_smoke_low_res_resize():
    """
    Smoke test resizing a low resolution artpack to match a high resolution
    artpack.
    """

    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-2x2-exact']
    image_location_list = floor1.get_image_location_list(0, 0)

    low_res_assetpack = AssetpackFactory.load('assetpacks/low_res_isometric')
    low_res_assetpack.resize_images(assetpack.projection)
    low_res_floor = low_res_assetpack.components[
        'easy-dungeon-ddl-example-iso-lowres.floor-2x2-low-res']
    image_location_list6 = low_res_floor.get_image_location_list(1, 1)
    image_pixel_list6 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list6)

    renderer6 = Renderer(image_pixel_list=image_pixel_list6)
    renderer6.add_image_pixel_list(
        image_pixel_list=assetpack.projection
        .get_image_pixel_list(0, 0, image_location_list))
    renderer6.output('file', filepath='tests/test_outputs/low_res_iso.png')
    with open("tests/test_outputs/low_res_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '07d5e0cc5eff5d1fadcb80027b0e52fb'


def test_non_scaled_rendering():
    """Tests rescaling by mashing together a prop pack of one scale and
    a floor pack of a different one."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor_1x1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-1x1-exact']
    image_location_list7_3 = floor_1x1.get_image_location_list(0, 0)
    image_pixel_list7_3 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_3)

    prop_assetpack = AssetpackFactory.load('assetpacks/example_props')
    boxes = prop_assetpack.components['easy-dungeon-ddl-example-props.many-boxes']
    image_location_list7_2 = boxes.get_image_location_list(0, 0)
    # Needs relocating to match the larger grid.
    image_pixel_list7_2 = prop_assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_2)

    renderer7 = Renderer(image_pixel_list=image_pixel_list7_2)
    renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7_3)
    renderer7.output('file', filepath='tests/test_outputs/nonscale_iso.png')
    with open("tests/test_outputs/nonscale_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '060bf51a9a174f710bb22726013f0c44'


def test_scaled_rendering():
    """Tests rescaling by rescaling a prop pack to match the projection
     of the floor pack."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    prop_assetpack2 = AssetpackFactory.load('assetpacks/example_props')
    prop_assetpack2.rescale_components(assetpack.projection)
    assetpack.append_assetpack(prop_assetpack2)

    data = {
        "name": '',
        "id": 'boxes_on_floor',
        "parts": [],
        "tags": []
    }
    boxes_on_floor = ComponentAsset(data, assetpack)
    boxes_on_floor.add_image(assetpack.images["easy-dungeon-ddl-example-iso.floor-1x1-exact"], 0, 0)
    boxes_on_floor.add_component(prop_assetpack2.components["easy-dungeon-ddl-example-props.many-boxes"], 0, 0)

    image_location_list7_1 = boxes_on_floor.get_image_location_list(0, 0)

    image_pixel_list7_1 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_1)

    renderer8 = Renderer(image_pixel_list=image_pixel_list7_1)
    renderer8.output('file', filepath='tests/test_outputs/scale_iso.png')
    with open("tests/test_outputs/scale_iso.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '0ed23a9f8ccd16b278678881a30b6792'
