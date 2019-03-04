"""Runs tests to ensure the code runs through.
 Coverage unknown, no unit tests yet. Prints pretty pictures though."""

from ddl import ArtpackFactory, BlueprintFactory, Renderer, Positioner

artpack = ArtpackFactory.load('example_isometric')
positioner = Positioner(artpack.artpack['grid'])
floor1 = artpack.blueprints['floor_2x2_exact']
image_location_list = floor1.get_image_location_list(0, 0, artpack)
renderer = Renderer(image_pixel_list=positioner
                    .get_image_pixel_list(500, 0, image_location_list))
renderer.render()

assetfac = BlueprintFactory(artpack, "isometric")
assetfac.new_blueprint('floor_1x2_exact', 'floor')
assetfac.add_image("floor_1x1_exact", 0, 0)
assetfac.add_image("floor_1x1_exact", 0, 1)
floor4 = assetfac.pull_blueprint()

assetfac.new_blueprint('twiddle_1', 'floor')
assetfac.add_blueprint("floor_2x2_exact", 0, 0)
assetfac.add_image("floor_1x1_exact", 2, 1)
assetfac.add_image("floor_1x1_exact", 2, 2)
assetfac.add_image("floor_1x1_exact", 2, 3)
assetfac.add_blueprint("floor_2x2_exact", 3, 3)
floor5 = assetfac.pull_blueprint()

print(floor5.get_image_location_list(1, 1, artpack))
image_location_list2 = floor4.get_image_location_list(0, 0, artpack)
image_pixel_list2 = positioner.get_image_pixel_list(500, 0,
                                                    image_location_list2)
renderer2 = Renderer(image_pixel_list=image_pixel_list2)
renderer2.render()


image_location_list3 = floor5.get_image_location_list(0, 0, artpack)
image_pixel_list3 = positioner.get_image_pixel_list(500, 0,
                                                    image_location_list3)
renderer3 = Renderer(image_pixel_list=image_pixel_list3)
renderer3.render()

assetfac.new_blueprint('fuzzy', 'floor')
assetfac.add_image("floor_1x1_exact", 0, 0)
assetfac.add_image("floor_1x1_fuzzy", 0, 1)
assetfac.add_image("floor_1x1_fuzzy", 1, 0)
assetfac.add_image("floor_1x1_exact", 1, 1)
fuzzy = assetfac.pull_blueprint()

renderer4 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
    500, 500, fuzzy.get_image_location_list(0, 0, artpack)))
renderer4.render()

assetfac.new_blueprint('wall', 'wall')
assetfac.add_image("floor_1x1_exact", 0, 0)
assetfac.add_image("exact_wall_1", 0, 0)
wall = assetfac.pull_blueprint()

renderer5 = Renderer(image_pixel_list=positioner.get_image_pixel_list(
    500, 500, wall.get_image_location_list(0, 0, artpack)))
renderer5.render()

# Will alter all of low_res_artpack's images to be the same size as artpack's
low_res_artpack = ArtpackFactory.load('low_res_isometric')
low_res_artpack.resize_images(artpack.artpack['grid'])
low_res_floor = low_res_artpack.blueprints['floor_2x2_low_res']
image_location_list6 = low_res_floor.get_image_location_list(1, 1,
                                                             low_res_artpack)
image_pixel_list6 = positioner.get_image_pixel_list(500, 0,
                                                    image_location_list6)
# toto: Why is this backwards?
renderer6 = Renderer(image_pixel_list=image_pixel_list6)
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
