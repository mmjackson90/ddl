"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl import AssetpackFactory, ComponentFactory, Positioner
from ddl.renderer import Renderer

ASSETPACK = AssetpackFactory.load('example_isometric')
POSITIONER = Positioner(ASSETPACK.grid)
FLOOR1 = ASSETPACK.components['floor-2x2-exact']
IMAGE_LOCATION_LIST = FLOOR1.get_image_location_list(0, 0, ASSETPACK)
RENDERER = Renderer(image_pixel_list=POSITIONER
                    .get_image_pixel_list(0, 0, IMAGE_LOCATION_LIST))
RENDERER.output('screen')

COMPONENT_FACTORY = ComponentFactory(ASSETPACK, "isometric")
COMPONENT_FACTORY.new_component('floor-1x2-exact', 'floor')
COMPONENT_FACTORY.add_image("floor-1x1-exact", 0, 0)
COMPONENT_FACTORY.add_image("floor-1x1-exact", 0, 1)
FLOOR4 = COMPONENT_FACTORY.pull_component()

IMAGE_LOCATION_LIST2 = FLOOR4.get_image_location_list(0, 0, ASSETPACK)
IMAGE_PIXEL_LIST2 = POSITIONER.get_image_pixel_list(0, 0, IMAGE_LOCATION_LIST2)
RENDERER2 = Renderer(image_pixel_list=IMAGE_PIXEL_LIST2)
RENDERER2.output('screen')


COMPONENT_FACTORY.new_component('twiddle_1', 'floor')
COMPONENT_FACTORY.add_component("floor-2x2-exact", 0, 0)
COMPONENT_FACTORY.add_image("floor-1x1-exact", 2, 1)
COMPONENT_FACTORY.add_image("floor-1x1-exact", 2, 2)
COMPONENT_FACTORY.add_image("floor-1x1-exact", 2, 3)
COMPONENT_FACTORY.add_component("floor-2x2-exact", 3, 3)
COMPONENT_FACTORY.add_image("floor-1x1-fuzzy", 4, 4)
COMPONENT_FACTORY.remove_last_part()
COMPONENT_FACTORY.output_component()
COMPONENT_FACTORY.clear_component()

COMPONENT_FACTORY.new_component('fuzzy', 'floor')
COMPONENT_FACTORY.add_image("floor-1x1-exact", 0, 0)
COMPONENT_FACTORY.add_image("floor-1x1-fuzzy", 0, 1)
COMPONENT_FACTORY.add_image("floor-1x1-fuzzy", 1, 0)
COMPONENT_FACTORY.add_image("floor-1x1-exact", 1, 1)
COMPONENT_FACTORY.print_component()
FUZZY = COMPONENT_FACTORY.pull_component()

RENDERER4 = Renderer(image_pixel_list=POSITIONER.get_image_pixel_list(
    0, 0, FUZZY.get_image_location_list(0, 0, ASSETPACK)))
RENDERER4.output('screen')

COMPONENT_FACTORY.new_component('wall', 'wall')
COMPONENT_FACTORY.add_image("floor-1x1-exact", 0, 0)
COMPONENT_FACTORY.add_image("exact-wall-1", 0, 0)
WALL = COMPONENT_FACTORY.pull_component()

RENDERER5 = Renderer(image_pixel_list=POSITIONER.get_image_pixel_list(
    0, 0, WALL.get_image_location_list(0, 0, ASSETPACK)))
RENDERER5.output('screen')

# Will alter all of low_res_assetpacks images to be the same size as assetpacks
LOW_RES_ASSETPACK = AssetpackFactory.load('low_res_isometric')
LOW_RES_ASSETPACK.resize_images(ASSETPACK.grid)
LOW_RES_FLOOR = LOW_RES_ASSETPACK.components['floor-2x2-low-res']
IMAGE_LOCATION_LIST6 = LOW_RES_FLOOR.get_image_location_list(1, 1,
                                                             LOW_RES_ASSETPACK)
IMAGE_PIXEL_LIST6 = POSITIONER.get_image_pixel_list(0, 0,
                                                    IMAGE_LOCATION_LIST6)
# toto: Why is this backwards?
RENDERER6 = Renderer(image_pixel_list=IMAGE_PIXEL_LIST6)
RENDERER6.add_image_pixel_list(
    image_pixel_list=POSITIONER
    .get_image_pixel_list(0, 0, IMAGE_LOCATION_LIST))
RENDERER6.output('screen')

# Adds in tiny boxes using a native grid (1 square =1/10th the big grid)
# Then rescales the assetpack and adds in the same component on the big grid
# much more accurately.
PROP_ASSETPACK = AssetpackFactory.load('example_props')
BOXES = PROP_ASSETPACK.components['many-boxes']
IMAGE_LOCATION_LIST7 = BOXES.get_image_location_list(0, 0, PROP_ASSETPACK)
POSITIONER2 = Positioner(PROP_ASSETPACK.grid)
IMAGE_PIXEL_LIST7 = POSITIONER2.get_image_pixel_list(0, 0,
                                                     IMAGE_LOCATION_LIST7)


PROP_ASSETPACK.rescale_pack(ASSETPACK.grid)
IMAGE_LOCATION_LIST7_1 = BOXES.get_image_location_list(0, 1, PROP_ASSETPACK)

IMAGE_PIXEL_LIST7_1 = POSITIONER.get_image_pixel_list(0, 0,
                                                      IMAGE_LOCATION_LIST7_1)
# todo: Why is this backwards?
RENDERER7 = Renderer(image_pixel_list=IMAGE_PIXEL_LIST7_1)
RENDERER7.add_image_pixel_list(image_pixel_list=IMAGE_PIXEL_LIST7)
RENDERER7.add_image_pixel_list(
    image_pixel_list=POSITIONER
    .get_image_pixel_list(0, 0, IMAGE_LOCATION_LIST))
RENDERER7.output('screen')
