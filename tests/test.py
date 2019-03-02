from PIL import Image
import json
import math

import sys
sys.path.append('../')

from ddl.ddl import ArtpackFactory, AssetFactory, Renderer

artpack = ArtpackFactory.load('example_isometric')
floor = artpack.assets['floor_1x1_exact']
floor2 = artpack.assets['floor_1x1_fuzzy']
floor3 = artpack.assets['floor_2x2_exact']
renderer = Renderer()
renderer.add_asset(floor3,500,0,artpack)
renderer.render()


assetfac=AssetFactory(artpack,artpack.data["grid"])
assetfac.new_asset('floor_1x2_exact','floor')
assetfac.add_asset("floor_1x1_exact",0,0)
assetfac.add_asset("floor_1x1_exact",0,1)
floor4=assetfac.spy_asset()

renderer2 = Renderer(sub_assets=floor4.get_sub_assets(500,0,artpack))
renderer2.render()
