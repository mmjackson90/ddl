"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl.assetpack import AssetpackFactory
from ddl.renderer import Renderer
from ddl.asset import ComponentAsset
import hashlib


def test_smoke_render_component():
    """
    Smoke test loading and rendering a component with multiple
    images that came from a definition.
    """

    assetpack = AssetpackFactory.load('assetpacks/example_top_down')
    floor1 = assetpack.components['easy-dungeon-ddl-example-td.floor-2x2-exact']
    image_location_list = floor1.get_image_location_list(0, 0)

    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('file', filepath='tests/test_outputs/floor1_td.png')
    with open("tests/test_outputs/floor1_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == 'bdf186aafd307763633ff0d082762126'


def test_smoke_design_component():
    """
    Smoke test creating a new component and then passing it to a renderer.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')
    data = {
        "name": '',
        "id": 'floor-1x2-exact',
        "parts": [],
        "tags": []
    }
    floor4 = ComponentAsset(data, assetpack)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 0, 0)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 0, 1)

    image_location_list2 = floor4.get_image_location_list(0, 0)
    image_pixel_list2 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list2)
    renderer2 = Renderer(image_pixel_list=image_pixel_list2)
    renderer2.output('file', filepath='tests/test_outputs/floor4_td.png')
    with open("tests/test_outputs/floor4_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '66add2fc4e1f7858e6452f8edaa9f52b'


def test_smoke_twiddly():
    """
    Smoke test creating a new component, removing a bit, and then using the
    component factory's built in output method to render it, before testing the
    clear component functionality and finally rendering out some fuzzy tiles.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')

    data = {
        "name": '',
        "id": 'twiddle_1',
        "parts": [],
        "tags": []
    }
    floor4 = ComponentAsset(data, assetpack)
    floor4.add_component(assetpack.components["easy-dungeon-ddl-example-td.floor-2x2-exact"], 0, 0)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 2, 1)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 2, 2)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 2, 3)
    floor4.add_component(assetpack.components["easy-dungeon-ddl-example-td.floor-2x2-exact"], 3, 3)
    floor4.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-fuzzy"], 4, 4)
    floor4.remove_last_part()
    renderer4_1 = Renderer(image_pixel_list=assetpack.projection.
                           get_image_pixel_list(0, 0, floor4.get_image_location_list(0, 0)))
    renderer4_1.output('file', filepath='tests/test_outputs/twiddly_td.png')
    with open("tests/test_outputs/twiddly_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '7489ed37fe74fef3cf8ba10c2fae390b'


def test_smoke_fuzzy():
    """
    Smoke test creating a new component, removing a bit, and then using the
    component factory's built in output method to render it, before testing the
    clear component functionality and finally rendering out some fuzzy tiles.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')

    data = {
        "name": '',
        "id": 'fuzzy',
        "parts": [],
        "tags": []
    }
    fuzzy = ComponentAsset(data, assetpack)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 0, 0)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-fuzzy"], 0, 1)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-fuzzy"], 1, 0)
    fuzzy.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 1, 1)

    renderer4_2 = Renderer(image_pixel_list=assetpack.projection.
                           get_image_pixel_list(0, 0, fuzzy.get_image_location_list(0, 0)))
    renderer4_2.output('file', filepath='tests/test_outputs/fuzzy_td.png')
    with open("tests/test_outputs/fuzzy_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '855c82a18da23146df083e9dae5e1315'


def test_smoke_wall():
    """
    Smoke test a wall/floor combo, just to check the offsets look good.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')
    asset_id = 'easy-dungeon-ddl-example-td.double-floor-wall-exact'
    floor_wall = assetpack.components[asset_id]
    ill = floor_wall.get_image_location_list(0, 0)
    assert ill[1][1:5] == (1, 1, True, False)
    renderer5 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, ill))

    renderer5.output('file', filepath='tests/test_outputs/wall_td.png')
    with open("tests/test_outputs/wall_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '008c60783924e6bfc1c7d7df61d2f69b'


def test_non_scaled_rendering():
    """Tests rescaling by mashing together a prop pack of one scale and
    a floor pack of a different one."""
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')
    floor_1x1 = assetpack.components['easy-dungeon-ddl-example-td.floor-1x1-exact']
    image_location_list7_3 = floor_1x1.get_image_location_list(0, 0)
    image_pixel_list7_3 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_3)

    prop_assetpack = AssetpackFactory.load('assetpacks/example_top_down_props')
    boxes = prop_assetpack.components['easy-dungeon-ddl-example-props-td.many-boxes']
    image_location_list7_2 = boxes.get_image_location_list(0, 0)
    # Needs relocating to match the larger grid.
    image_pixel_list7_2 = prop_assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_2)

    renderer7 = Renderer(image_pixel_list=image_pixel_list7_2)
    renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7_3)
    renderer7.output('file', filepath='tests/test_outputs/nonscaled_td.png')
    with open("tests/test_outputs/nonscaled_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '69af4842e8237eef44518eb85b8dbe9d'


def test_scaled_rendering():
    """Tests rescaling by rescaling a prop pack to match the projection
     of the floor pack."""
    assetpack = AssetpackFactory.load('assetpacks/example_top_down')
    prop_assetpack2 = AssetpackFactory.load('assetpacks/example_top_down_props')
    prop_assetpack2.rescale_components(assetpack.projection)
    assetpack.append_assetpack(prop_assetpack2)

    data = {
        "name": '',
        "id": 'fuzzy',
        "parts": [],
        "tags": []
    }
    boxes_on_floor = ComponentAsset(data, assetpack)
    boxes_on_floor.add_image(assetpack.images["easy-dungeon-ddl-example-td.floor-1x1-exact"], 0, 0)
    boxes_on_floor.add_component(assetpack.components["easy-dungeon-ddl-example-props-td.many-boxes"], 0, 0)
    image_location_list7_1 = boxes_on_floor.\
        get_image_location_list(0, 0)

    image_pixel_list7_1 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_1)

    renderer8 = Renderer(image_pixel_list=image_pixel_list7_1)
    renderer8.output('file', filepath='tests/test_outputs/scaled_td.png')
    with open("tests/test_outputs/scaled_td.png", "rb") as output_blueprint:
        data = output_blueprint.read()
        md5 = hashlib.md5(data).hexdigest()
    assert md5 == '69af4842e8237eef44518eb85b8dbe9d'
