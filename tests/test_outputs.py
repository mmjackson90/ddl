"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl import AssetpackFactory, ComponentFactory, Positioner
from ddl.renderer import Renderer


def test_old_tests():
    """
    Old Tests

    Our old, rough and ready tests.
    """

    assetpack = AssetpackFactory.load('example_isometric')
    positioner = Positioner(assetpack.grid)
    floor1 = assetpack.components['floor-2x2-exact']
    image_location_list = floor1.get_image_location_list(0, 0, assetpack)

    renderer = Renderer(image_pixel_list=positioner
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('screen')

    component_factory = ComponentFactory(assetpack, "isometric")
    component_factory.new_component('floor-1x2-exact', 'floor')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("floor-1x1-exact", 0, 1)
    floor4 = component_factory.pull_component()

    image_location_list2 = floor4.get_image_location_list(0, 0, assetpack)
    image_pixel_list2 = positioner.get_image_pixel_list(0, 0, image_location_list2)
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

    renderer4 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
        0, 0, fuzzy.get_image_location_list(0, 0, assetpack)))
    renderer4.output('screen')

    component_factory.new_component('wall', 'wall')
    component_factory.add_image("floor-1x1-exact", 0, 0)
    component_factory.add_image("exact-wall-1", 0, 0)
    wall = component_factory.pull_component()

    renderer5 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
        0, 0, wall.get_image_location_list(0, 0, assetpack)))
    renderer5.output('screen')

    # Will alter all of low_res_assetpacks images to be the same size as assetpacks
    low_res_assetpack = AssetpackFactory.load('low_res_isometric')
    low_res_assetpack.resize_images(assetpack.grid)
    low_res_floor = low_res_assetpack.components['floor-2x2-low-res']
    image_location_list6 = low_res_floor.get_image_location_list(1, 1,
                                                                 low_res_assetpack)
    image_pixel_list6 = positioner.get_image_pixel_list(0, 0,
                                                        image_location_list6)
    # toto: Why is this backwards?
    renderer6 = Renderer(image_pixel_list=image_pixel_list6)
    renderer6.add_image_pixel_list(
        image_pixel_list=positioner
        .get_image_pixel_list(0, 0, image_location_list))
    renderer6.output('screen')

    # Adds in tiny boxes using a native grid (1 square =1/10th the big grid)
    # Then rescales the assetpack and adds in the same component on the big grid
    # much more accurately.
    prop_assetpack = AssetpackFactory.load('example_props')
    boxes = prop_assetpack.components['many-boxes']
    image_location_list7 = boxes.get_image_location_list(0, 0, prop_assetpack)
    positioner2 = Positioner(prop_assetpack.grid)
    image_pixel_list7 = positioner2.get_image_pixel_list(0, 0,
                                                         image_location_list7)


    prop_assetpack.rescale_pack(assetpack.grid)
    image_location_list7_1 = boxes.get_image_location_list(0, 1, prop_assetpack)

    image_pixel_list7_1 = positioner.get_image_pixel_list(0, 0,
                                                          image_location_list7_1)
    # todo: Why is this backwards?
    renderer7 = Renderer(image_pixel_list=image_pixel_list7_1)
    renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7)
    renderer7.add_image_pixel_list(
        image_pixel_list=positioner
        .get_image_pixel_list(0, 0, image_location_list))
    renderer7.output('screen')
