"""
The assetpack and assetpack factory methods.
"""

import json
import os

from ddl.projection import IsometricProjection, TopDownProjection
from ddl.asset import ComponentAsset, ImageAsset
from ddl.taglist import TagList
from ddl.validator import Validator


class ProjectionTypeException(Exception):
    """Exception class for if two projections dont share a type"""
    pass


class ProjectionGridException(Exception):
    """Exception class for if two projections dont share grid sizes"""
    pass


class AssetpackFactory:
    """A factory for creating AssetPacks"""
    @staticmethod
    def load(path):
        """
        Validates and loads AssetPacks from their component and Image packs,
        given an appropriate name
        """

        pack_path = os.path.abspath(path)

        Validator.validate_file(pack_path + '/pack.json',
                                'pack')
        Validator.validate_file(pack_path + '/images.json',
                                'images')
        Validator.validate_file(pack_path + '/components.json',
                                'components')
        with open(
                pack_path + '/components.json'
                ) as component_file, open(
                pack_path + '/images.json'
                ) as imagepack_file:
            components_and_grid = json.load(component_file)
            imagepack = json.load(imagepack_file)

            pack_id = path.split('/')[-1]

            return Assetpack(pack_id, pack_path, imagepack, components_and_grid)


class Assetpack:
    """This class records all information needed to
     position and render the various images located in an assetpack.
     Please see the assetpack and imagepack schema for more info"""
    def __init__(self, pack_id, pack_path, imagepack, components_and_grid):

        self.components = {}
        self.images = {}
        self.pack_id = pack_id
        self.pack_path = pack_path
        self.grid = components_and_grid['grid']
        self.taglist = TagList()
        if self.grid['type'] == 'isometric':
            self.projection = IsometricProjection(self.grid['width'],
                                                  self.grid['height'])
        else:
            self.projection = TopDownProjection(self.grid['width'],
                                                self.grid['height'])

        for image in imagepack['images']:
            new_image = ImageAsset(image, assetpack_id=pack_id, assetpack_path=pack_path)
            self.add_image(new_image)

        for component in components_and_grid['components']:
            new_component = ComponentAsset(component, assetpack_id=pack_id)
            self.taglist.add_component(new_component)
            self.add_component(new_component)

    def add_component(self, new_asset):
        """Adds a component to the componentlist, if it doesn't exist"""
        if self.components.setdefault(new_asset.get_full_id(),
                                      new_asset) != new_asset:
            raise ValueError('''The key %s is overloaded. Please ensure no\
 components share IDs''' % new_asset.get_full_id())

    def add_image(self, new_asset):
        """Adds an image to the imagelist, if it doesn't already exist"""
        if self.images.setdefault(new_asset.get_full_id(),
                                  new_asset) != new_asset:
            raise ValueError('''The key %s is overloaded. Please ensure no\
 images share IDs''' % new_asset.get_full_id())

    def append_assetpack(self, assetpack):
        """
        Checks two assetpacks can be added together, then sticks one
        assetpack atop the previous one.
        """
        if not isinstance(self.projection, type(assetpack.projection)):
            raise ProjectionTypeException()
        if self.projection.width != assetpack.projection.width:
            raise ProjectionGridException()
        if self.projection.width != assetpack.projection.width:
            raise ProjectionGridException()

        for image in assetpack.images.values():
            self.add_image(image)
        for component in assetpack.components.values():
            self.add_component(component)

        self.taglist.append(assetpack.taglist)

    def change_assetpack_id(self, new_id):
        """
        Changes the name of the assetpack and all asset's assetpack
        identifiers.
        """
        new_images = self.images
        new_components = self.components
        self.images = {}
        self.components = {}
        for component in new_components.values():
            component.assetpack_id = new_id
            component.reset_sub_parts()
            self.add_component(component)
        for image in new_images.values():
            image.assetpack_id = new_id
            image.reset_sub_parts()
            self.add_image(image)
        self.pack_id = new_id

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

    def get_image_location_list(self, offset_x, offset_y, component):
        """
        For a given component, recurses down it's tree of parts until we end
        up with nothing but a list of images and their absolute (by grid)
        offsets
        """
        part_list = component.get_part_list(offset_x, offset_y)
        image_location_list = []
        for asset_type, asset_id, part_offset_x, part_offset_y in part_list:
            if asset_type == "image":
                sub_image = self.images[asset_id]
                image_location_list = image_location_list+[(
                    sub_image, part_offset_x, part_offset_y
                )]
            else:
                sub_component = self.components[asset_id]
                new_ill = self.get_image_location_list(part_offset_x,
                                                       part_offset_y,
                                                       sub_component)
                image_location_list = image_location_list+new_ill
        return image_location_list
