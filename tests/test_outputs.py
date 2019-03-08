"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl import AssetpackFactory, ComponentFactory
from ddl.renderer import Renderer


def test_old_tests():
    """
    Old Tests

    Our old, rough and ready tests.
    """

    assetpack = AssetpackFactory.load('example_isometric')
    floor1 = assetpack.components['floor-2x2-exact']
    image_location_list = floor1.get_image_location_list(0, 0, assetpack)

    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('screen')

    component_factory = ComponentFactory(assetpack, "isometric")
    component_factory.new_component('floor-1x2-exact', 'floor')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("floor-1x1-exact", 0, 1)
    floor4 = component_factory.pull_component()

    image_location_list2 = floor4.get_image_location_list(0, 0, assetpack)
    image_pixel_list2 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list2)
    renderer2 = Renderer(image_pixel_list=image_pixel_list2)
    renderer2.output('screen')

    component_factory.new_component('twiddle_1', 'floor')
    component_factory.add_component("floor-2x2-exact", 0, 0)
    component_factory.add_image("floor-1x1-exact", 2, 1)
    component_factory.add_image("floor-1x1-exact", 2, 2)
    component_factory.add_image("floor-1x1-exact", 2, 3)
    component_factory.add_component("floor-2x2-exact", 3, 3)
    component_factory.add_image("floor-1x1-fuzzy", 4, 4)
    component_factory.remove_last_part()
    component_factory.output_component()
    component_factory.clear_component()

    component_factory.new_component('fuzzy', 'floor')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("floor-1x1-fuzzy", 0, 1)
    component_factory.add_image("floor-1x1-fuzzy", 1, 0)
    component_factory.add_image("floor-1x1-exact", 1, 1)
    component_factory.print_component()
    fuzzy = component_factory.pull_component()

    renderer4 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, fuzzy.
                                              get_image_location_list(0, 0,
                                                                      assetpack
                                                                      )))
    renderer4.output('screen')

    component_factory.new_component('wall', 'wall')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("exact-wall-1", 0, 0)
    wall = component_factory.pull_component()

    renderer5 = Renderer(image_pixel_list=assetpack.projection.
                         get_image_pixel_list(0, 0, wall.
                                              get_image_location_list(0, 0,
                                                                      assetpack
                                                                      )))
    renderer5.output('screen')

    # Will alter all of low_res_assetpacks images
    # to be the same size as assetpacks
    low_res_assetpack = AssetpackFactory.load('low_res_isometric')
    low_res_assetpack.resize_images(assetpack.projection)
    low_res_floor = low_res_assetpack.components['floor-2x2-low-res']
    image_location_list6 = low_res_floor.\
        get_image_location_list(1, 1, low_res_assetpack)
    image_pixel_list6 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list6)
    # toto: Why is this backwards?
    renderer6 = Renderer(image_pixel_list=image_pixel_list6)
    renderer6.add_image_pixel_list(
        image_pixel_list=assetpack.projection
        .get_image_pixel_list(0, 0, image_location_list))
    renderer6.output('screen')

    # Adds in tiny boxes using a native grid (1 square =1/10th the big grid)
    # Then rescales the assetpack and adds in the same component on the big
    # grid much more accurately.


def test_non_scaled_rendering():
    """Tests rescaling by mashing together a prop pack of one scale and
    a floor pack of a different one."""
    assetpack = AssetpackFactory.load('example_isometric')
    floor_1x1 = assetpack.components['floor-1x1-exact']
    image_location_list7_3 = floor_1x1.get_image_location_list(0, 0,
                                                               assetpack)
    image_pixel_list7_3 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_3)

    prop_assetpack = AssetpackFactory.load('example_props')
    boxes = prop_assetpack.components['many-boxes']
    image_location_list7_2 = boxes.get_image_location_list(0, 0,
                                                           prop_assetpack)
    # Needs relocating to match the larger grid.
    image_pixel_list7_2 = prop_assetpack.projection.\
        get_image_pixel_list(-4, 5, image_location_list7_2)

    renderer7 = Renderer(image_pixel_list=image_pixel_list7_2)
    renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7_3)
    renderer7.output('screen')


def test_scaled_rendering():
    """Tests rescaling by rescaling a prop pack to match the projection
     of the floor pack."""
    assetpack = AssetpackFactory.load('example_isometric')
    floor_1x1 = assetpack.components['floor-1x1-exact']
    image_location_list7_3 = floor_1x1.get_image_location_list(0, 0,
                                                               assetpack)

    image_pixel_list7_3 = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list7_3)
    prop_assetpack2 = AssetpackFactory.load('example_props')
    prop_assetpack2.rescale_pack(assetpack.projection)
    boxes2 = prop_assetpack2.components['many-boxes']
    image_location_list7_1 = boxes2.\
        get_image_location_list(0, 0, prop_assetpack2)

    image_pixel_list7_1 = prop_assetpack2.projection.\
        get_image_pixel_list(0, 0, image_location_list7_1)

    renderer8 = Renderer(image_pixel_list=image_pixel_list7_1)
    renderer8.add_image_pixel_list(image_pixel_list7_3)
    renderer8.output('screen')
