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

        self.images = {}
        self.components = {}
        self.name = name
        self.grid = components_and_grid['grid']
        if self.grid['type'] == 'isometric':
            self.projection = IsometricProjection(self.grid['width'],
                                                  self.grid['height'])
        else:
            self.projection = TopDownProjection(self.grid['width'],
                                                self.grid['height'])

        for image in imagepack['images']:
            self.images[image['id']] = ImageAsset(image, assetpack_name=name)

        for component in components_and_grid['components']:
            self.components[component['id']] =\
                ComponentAsset(component, assetpack_name=name)

    def resize_images(self, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
         images in the assetpack to match up the grids.
         Actually scales images at the moment, but could just change scale
         factors"""
        self.projection.resize_images(self.images, desired_projection)
        self.projection.alter_grid_parameters(desired_projection)

    def rescale_components(self, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
        co-ordinates used in blueprints."""
        self.projection.rescale_components(self.components, desired_projection)
        self.projection.alter_grid_parameters(desired_projection)
