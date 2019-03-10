"""
Contains the Component class and ComponentFactory helper class
"""

import json
from PIL import Image


class Asset:
    """
    The superclass for components and images. Implements methods common to
    both to allow for easier implementation of global asset lists.
    """
    def __init__(self, data, assetpack_name):
        self.data = data
        self.assetpack_name = assetpack_name
        self.name = data['name']
        self.asset_id = data['id']

    def get_full_id(self):
        """Default. Should always be overriden"""
        return (self.assetpack_name + '.' + self.asset_id)

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Passes. Implementations of this method exists in subclasses"""
        pass

    def resize(self, size_ratio_x, size_ratio_y):
        """Passes. Implementations of this method exists in subclasses"""
        pass


class ComponentAsset(Asset):
    """This is a space saving measure that records
     multiple image_assets and components (collectively known as assets)
     and their respective positions within the Asset Pack's grid."""
    def __init__(self, data, assetpack_name):
        super().__init__(data, assetpack_name)
        if "parts" in data.keys():
            self.parts = data["parts"]
            for sub_part in self.parts:
                sub_part["asset_id"] = self.get_part_full_id(sub_part)
        else:
            raise Exception('Component {} has no parts.',
                            self.data["name"])

    def get_image_location_list(self, offset_x, offset_y, assetpack):
        """Recursively moves down a component, finally returning a list of
         images and their offsets, given some already known pixel offset
         values."""
        image_location_list = []
        for sub_asset in self.parts:
            sub_component = assetpack.assets[sub_asset["asset_id"]]
            sub_offset_x = sub_asset["x"]+offset_x
            sub_offset_y = sub_asset["y"]+offset_y
            new_ill = sub_component.get_image_location_list(
                                                      sub_offset_x,
                                                      sub_offset_y,
                                                      assetpack)
            image_location_list = image_location_list+new_ill
        return image_location_list

    def get_part_full_id(self, sub_part):
        if sub_part['type'] == 'image':
            return(self.assetpack_name + '.i.' + sub_part["image_id"])
        else:
            return(self.assetpack_name + '.c.' + sub_part["component_id"])

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Alters all the co-ordinates in a blueprint to match a new
         co-ordinate system."""
        for sub_asset in self.data["parts"]:
            sub_asset["x"] = sub_asset["x"] / scale_ratio_x
            sub_asset["y"] = sub_asset["y"] / scale_ratio_y

    def get_full_id(self):
        """Returns the ID of this component"""
        return (self.assetpack_name + '.c.' + self.asset_id)


class ImageAsset(Asset):
    """A representation of an actual image file and the pixel offsets required
     to put it in the correct location."""
    def __init__(self, data, assetpack_name):
        super().__init__(data, assetpack_name)
        if "top_left" in data.keys():
            self.top_left = data["top_left"]
        else:
            self.top_left = {"x": 0, "y": 0}

        self.image = Image.open('assetpacks/' + assetpack_name + '/art/' +
                                data["image"])

    def resize(self, size_ratio_x, size_ratio_y):
        """Alters the image and it's top_left pixel offsets by some x and y
         scale factors"""
        final_image_width = round(self.image.width*size_ratio_x)
        final_image_height = round(self.image.height*size_ratio_y)
        self.image = self.image.resize((final_image_width, final_image_height))
        self.top_left['x'] = round(self.top_left['x']*size_ratio_x)
        self.top_left['y'] = round(self.top_left['y']*size_ratio_y)

    def show(self):
        """Show the image."""
        self.image.show()

    def get_image_location_list(self, offset_x, offset_y, assetpack):
        """The leaf end of a component call for image lists."""
        return([(self, offset_x, offset_y)])

    def get_full_id(self):
        """Returns the ID of this component"""
        return (self.assetpack_name + '.i.' + self.asset_id)
