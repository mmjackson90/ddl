from PIL import Image
import json
import math

from ddl import ArtpackFactory, BlueprintFactory, Renderer

artpack = ArtpackFactory.load('example_isometric')
test = Renderer(sub_assets=artpack.blueprints['floor_2x2_exact'].get_sub_assets(500,0,artpack))
test.render()

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

renderer2 = Renderer(sub_assets=floor4.get_sub_assets(500,0,artpack))
renderer2.render()

renderer3 = Renderer(sub_assets=floor5.get_sub_assets(500,0,artpack))
renderer3.render()
