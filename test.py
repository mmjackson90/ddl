"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl import AssetpackFactory, ComponentFactory, Renderer, Positioner

assetpack = AssetpackFactory.load('example_isometric')
positioner = Positioner(assetpack.grid)
floor1 = assetpack.components['floor_2x2_exact']
image_location_list = floor1.get_image_location_list(0, 0, assetpack)
renderer = Renderer(image_pixel_list=positioner
                    .get_image_pixel_list(500, 0, image_location_list))
renderer.render()

component_fac = ComponentFactory(assetpack, "isometric")
component_fac.new_component('floor_1x2_exact', 'floor')
component_fac.add_image("floor_1x1_exact", 0, 0)
component_fac.add_image("floor_1x1_exact", 0, 1)
floor4 = component_fac.pull_component()

component_fac.new_component('twiddle_1', 'floor')
component_fac.add_component("floor_2x2_exact", 0, 0)
component_fac.add_image("floor_1x1_exact", 2, 1)
component_fac.add_image("floor_1x1_exact", 2, 2)
component_fac.add_image("floor_1x1_exact", 2, 3)
component_fac.add_component("floor_2x2_exact", 3, 3)
floor5 = component_fac.pull_component()

print(floor5.get_image_location_list(1, 1, assetpack))
image_location_list2 = floor4.get_image_location_list(0, 0, assetpack)
image_pixel_list2 = positioner.get_image_pixel_list(500, 0,
                                                    image_location_list2)
renderer2 = Renderer(image_pixel_list=image_pixel_list2)
renderer2.render()


image_location_list3 = floor5.get_image_location_list(0, 0, assetpack)
image_pixel_list3 = positioner.get_image_pixel_list(500, 0,
                                                    image_location_list3)
renderer3 = Renderer(image_pixel_list=image_pixel_list3)
renderer3.render()

component_fac.new_component('fuzzy', 'floor')
component_fac.add_image("floor_1x1_exact", 0, 0)
component_fac.add_image("floor_1x1_fuzzy", 0, 1)
component_fac.add_image("floor_1x1_fuzzy", 1, 0)
component_fac.add_image("floor_1x1_exact", 1, 1)
fuzzy = component_fac.pull_component()

renderer4 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
    500, 500, fuzzy.get_image_location_list(0, 0, assetpack)))
renderer4.render()

component_fac.new_component('wall', 'wall')
component_fac.add_image("floor_1x1_exact", 0, 0)
component_fac.add_image("exact_wall_1", 0, 0)
wall = component_fac.pull_component()

renderer5 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
    500, 500, wall.get_image_location_list(0, 0, assetpack)))
renderer5.render()

# Will alter all of low_res_assetpacks images to be the same size as assetpacks
low_res_assetpack = AssetpackFactory.load('low_res_isometric')
low_res_assetpack.resize_images(assetpack.grid)
low_res_floor = low_res_assetpack.components['floor_2x2_low_res']
image_location_list6 = low_res_floor.get_image_location_list(1, 1,
                                                             low_res_assetpack)
image_pixel_list_6 = positioner.get_image_pixel_list(500, 0,
                                                     image_location_list6)
# toto: Why is this backwards?
renderer6 = Renderer(image_pixel_list=image_pixel_list_6)
renderer6.add_image_pixel_list(
    image_pixel_list=positioner
    .get_image_pixel_list(500, 0, image_location_list))
renderer6.render()

# Adds in tiny boxes using a native grid (1 square =1/10th the big grid)
# Then rescales the assetpack and adds in the same component on the big grid
# much more accurately.
prop_artpack = ArtpackFactory.load('example_props')
boxes = prop_artpack.blueprints['many_boxes']
image_location_list7 = boxes.get_image_location_list(0, 0, prop_artpack)
positioner2 = Positioner(prop_artpack.artpack['grid'])
image_pixel_list7 = positioner2.get_image_pixel_list(632, 0,
                                                     image_location_list7)


prop_artpack.rescale_components(artpack.artpack['grid'])
image_location_list7_1 = boxes.get_image_location_list(0, 1, prop_artpack)

image_pixel_list7_1 = positioner.get_image_pixel_list(632, 0,
                                                      image_location_list7_1)
# todo: Why is this backwards?
renderer7 = Renderer(image_pixel_list=image_pixel_list7_1)
renderer7.add_image_pixel_list(image_pixel_list=image_pixel_list7)
renderer7.add_image_pixel_list(
    image_pixel_list=positioner
    .get_image_pixel_list(500, 0, image_location_list))
renderer7.render()
