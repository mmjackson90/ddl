from PIL import Image
import json
import math

from ddl import ArtpackFactory, BlueprintFactory, Renderer, Positioner

artpack = ArtpackFactory.load('example_isometric')
positioner = Positioner(artpack.artpack['grid'])
image_location_list=artpack.blueprints['floor_2x2_exact'].get_image_location_list(0,0,artpack)
renderer = Renderer(image_pixel_list=positioner.get_image_pixel_list(500,0,image_location_list))
renderer.render()

assetfac=BlueprintFactory(artpack,"isometric")
assetfac.new_blueprint('floor_1x2_exact','floor')
assetfac.add_image("floor_1x1_exact",0,0)
assetfac.add_image("floor_1x1_exact",0,1)
floor4=assetfac.pull_blueprint()

assetfac.new_blueprint('twiddle_1','floor')
assetfac.add_blueprint("floor_2x2_exact",0,0)
assetfac.add_image("floor_1x1_exact",2,1)
assetfac.add_image("floor_1x1_exact",2,2)
assetfac.add_image("floor_1x1_exact",2,3)
assetfac.add_blueprint("floor_2x2_exact",3,3)
floor5=assetfac.pull_blueprint()

print(floor5.get_image_location_list(1,1,artpack))

renderer2 = Renderer(image_pixel_list=positioner.get_image_pixel_list(500,0,floor4.get_image_location_list(0,0,artpack)))
renderer2.render()

renderer3 = Renderer(image_pixel_list=positioner.get_image_pixel_list(500,0,floor5.get_image_location_list(0,0,artpack)))
renderer3.render()
