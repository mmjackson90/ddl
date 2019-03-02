from PIL import Image
import json
import math

import sys
sys.path.append('../')

from ddl import ArtpackFactory, AssetFactory, Renderer

artpack = ArtpackFactory.load('example_isometric')
test = Renderer(sub_assets=artpack.blueprints['floor_2x2_exact'].get_sub_assets(500,0,artpack,294,170))
test.render()

assetfac=AssetFactory(artpack,artpack.data["grid"])
assetfac.new_asset('floor_1x2_exact','floor')
assetfac.add_asset("floor_1x1_exact",0,0)
assetfac.add_asset("floor_1x1_exact",0,1)
floor4=assetfac.spy_asset()

renderer2 = Renderer(sub_assets=floor4.get_sub_assets(500,0,artpack))
renderer2.render()
