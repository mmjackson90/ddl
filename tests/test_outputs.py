"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl.assetpack import AssetpackFactory
from ddl.helper_classes import ComponentFactory
from ddl.renderer import Renderer


def test_smoke_render_component():
    """
    Smoke test loading and rendering a component with multiple
    images that came from a definition.
    """

    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-2x2-exact']
    image_location_list = assetpack.get_image_location_list(0, 0, floor1)

    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('screen')


def test_smoke_design_component():
    """
    Smoke test creating a new component and then passing it to a renderer.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component_factory = ComponentFactory(assetpack, "isometric")
    component_factory.new_component('floor-1x2-exact')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("floor-1x1-exact", 0, 1)
    floor4 = component_factory.pull_component()

    image_location_list2 = assetpack.get_image_location_list(0, 0, floor4)
    image_pixel_list2 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list2)
    renderer2 = Renderer(image_pixel_list=image_pixel_list2)
    renderer2.output('screen')


def test_smoke_twiddly_fuzzy():
    """
    Smoke test creating a new component, removing a bit, and then using the
    component factory's built in output method to render it, before testing the
    clear component functionality and finally rendering out some fuzzy tiles.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component_factory = ComponentFactory(assetpack, "isometric")
    component_factory.new_component('twiddle_1')
    component_factory.add_component("floor-2x2-exact", 0, 0)
    component_factory.add_image("floor-1x1-exact", 2, 1)
    component_factory.add_image("floor-1x1-exact", 2, 2)
    component_factory.add_image("floor-1x1-exact", 2, 3)
    component_factory.add_component("floor-2x2-exact", 3, 3)
    component_factory.add_image("floor-1x1-fuzzy", 4, 4)
    component_factory.remove_last_part()
    component_factory.output_component()
    component_factory.clear_component()

    component_factory.new_component('fuzzy')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("floor-1x1-fuzzy", 0, 1)
    component_factory.add_image("floor-1x1-fuzzy", 1, 0)
    component_factory.add_image("floor-1x1-exact", 1, 1)

    fuzzy = component_factory.pull_component()

    renderer4 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, assetpack.
                                              get_image_location_list(0, 0,
                                                                      fuzzy
                                                                      )))
    renderer4.output('screen')


def test_smoke_wall():
    """
    Smoke test a wall/floor combo, just to check the offsets look good.
    """
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor_wall = assetpack.components['easy-dungeon-ddl-example-iso.floor-wall-exact']
    ill = assetpack.get_image_location_list(0, 0, floor_wall)
    renderer5 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, ill))

    renderer5.output('screen')


def test_smoke_low_res_resize():
    """
    Smoke test resizing a low resolution artpack to match a high resolution
    artpack.
    """

    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-2x2-exact']
    image_location_list = assetpack.get_image_location_list(0, 0, floor1)

    low_res_assetpack = AssetpackFactory.load('assetpacks/low_res_isometric')
    low_res_assetpack.resize_images(assetpack.projection)
    low_res_floor = low_res_assetpack.components[
        'easy-dungeon-ddl-example-iso-lowres.floor-2x2-low-res']
    image_location_list6 = low_res_assetpack.\
        get_image_location_list(1, 1, low_res_floor)
    image_pixel_list6 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list6)

    renderer6 = Renderer(image_pixel_list=image_pixel_list6)
    renderer6.add_image_pixel_list(
        image_pixel_list=assetpack.projection
        .get_image_pixel_list(0, 0, image_location_list))
    renderer6.output('screen')


def test_non_scaled_rendering():
    """Tests rescaling by mashing together a prop pack of one scale and
    a floor pack of a different one."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    floor_1x1 = assetpack.components['easy-dungeon-ddl-example-iso.floor-1x1-exact']
    image_location_list7_3 = assetpack.get_image_location_list(0, 0,
                                                               floor_1x1)
    image_pixel_list7_3 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_3)

    prop_assetpack = AssetpackFactory.load('assetpacks/example_props')
    boxes = prop_assetpack.components['easy-dungeon-ddl-example-props.many-boxes']
    image_location_list7_2 = prop_assetpack.get_image_location_list(0, 0,
                                                                    boxes)
    # Needs relocating to match the larger grid.
    image_pixel_list7_2 = prop_assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_2)

    renderer7 = Renderer(image_pixel_list=image_pixel_list7_2)
    renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7_3)
    renderer7.output('screen')


def test_scaled_rendering():
    """Tests rescaling by rescaling a prop pack to match the projection
     of the floor pack."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    prop_assetpack2 = AssetpackFactory.load('assetpacks/example_props')
    prop_assetpack2.rescale_components(assetpack.projection)
    assetpack.append_assetpack(prop_assetpack2)

    component_factory = ComponentFactory(assetpack, "isometric")
    component_factory.new_component('boxes_on_floor')
    component_factory.add_image('floor-1x1-exact', 0, 0)
    component_factory.add_component('many-boxes', 0, 0,
                                    assetpack_id='easy-dungeon-ddl-example-props')
    boxes_on_floor = component_factory.pull_component()
    image_location_list7_1 = assetpack.\
        get_image_location_list(0, 0, boxes_on_floor)

    image_pixel_list7_1 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_1)

    renderer8 = Renderer(image_pixel_list=image_pixel_list7_1)
    renderer8.output('screen')
