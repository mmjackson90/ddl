"""
Dungeon Description Language

Create all the functions currently in use by DDL.
Thus far this is only really the Artist code.
"""


import json
import math
from ddl.renderer import Renderer
from ddl.projection import IsometricProjection, TopDownProjection
from ddl.asset import ComponentAsset, ImageAsset


class AssetpackFactory:
    """A factory for creating AssetPacks"""
    @staticmethod
    def load(name):
        """Loads AssetPacks from their component and Image packs,
         given an appropriate name"""
        with open(
                'assetpacks/' + name + '/components.json'
                ) as component_file, open(
                'assetpacks/' + name + '/images.json'
                ) as imagepack_file:
            components_and_grid = json.load(component_file)
            imagepack = json.load(imagepack_file)
            return Assetpack(name, imagepack, components_and_grid)


class Assetpack:
    """This class records all information needed to
     position and render the various images located in an assetpack.
     Please see the assetpack and imagepack schema for more info"""
    def __init__(self, name, imagepack, components_and_grid):

        self.assets = {}
        self.name = name
        self.grid = components_and_grid['grid']
        if self.grid['type'] == 'isometric':
            self.projection = IsometricProjection(self.grid['width'],
                                                  self.grid['height'])
        else:
            self.projection = TopDownProjection(self.grid['width'],
                                                self.grid['height'])

        for image in imagepack['images']:
            new_asset = ImageAsset(image, assetpack_name=name)
            self.add_asset(new_asset)

        for component in components_and_grid['components']:
            new_asset = ComponentAsset(component, assetpack_name=name)
            self.add_asset(new_asset)

    def add_asset(self, new_asset):
        """Adds an asset to the assetlist, if it doesn't already exist"""
        if self.assets.setdefault(new_asset.get_full_id(),
                                  new_asset) != new_asset:
            raise ValueError('''The key %s is overloaded. Please ensure no\
 assets share IDs''' % new_asset.get_full_id())

    def append_assetpack(self, assetpack):
        """
        Checks two assetpacks can be added together, then sticks one
        assetpack atop the previous one.
        """
        if not isinstance(self.projection, type(assetpack.projection)):
            raise Exception('''These two assetpacks do not share the same\
projection type. They cannot be combined''')
        grid_error = '''These two assetpacks do not share a grid height and\
width. Please resize or rescale to make sure the projections match.'''
        if self.projection.width != assetpack.projection.width:
            raise Exception(grid_error)
        if self.projection.width != assetpack.projection.width:
            raise Exception(grid_error)

        for asset in assetpack.assets.values():
            self.add_asset(asset)

    def change_assetpack_name(self, new_name):
        """
        Changes the name of the assetpack and all asset's assetpack
        identifiers.
        """
        new_assets = self.assets
        self.assets = {}
        for asset in new_assets.values():
            asset.assetpack_name = new_name
            asset.reset_sub_parts()
            self.add_asset(asset)
        self.name = new_name


    def resize_images(self, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
         images in the assetpack to match up the grids.
         Actually scales images at the moment, but could just change scale
         factors"""
        self.projection.resize_images(self.assets, desired_projection)
        self.projection.alter_grid_parameters(desired_projection)

    def rescale_components(self, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
        co-ordinates used in blueprints."""
        self.projection.rescale_components(self.assets, desired_projection)
        self.projection.alter_grid_parameters(desired_projection)
