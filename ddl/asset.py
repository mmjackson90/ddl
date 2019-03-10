"""
Contains the Component class and ComponentFactory helper class
"""

import json
from PIL import Image


class ComponentAsset:
    """This is a space saving measure that records
     multiple image_assets and components (collectively known as assets)
     and their respective positions within the Asset Pack's grid."""
    def __init__(self, data, assetpack_name):
        self.data = data
        # The assetpack this component is a part of
        self.assetpack_name = assetpack_name
        if "parts" in data.keys():
            self.parts = data["parts"]
        else:
            raise Exception('Component {} has no parts.',
                            self.data["name"])

    def get_image_location_list(self, offset_x, offset_y, assetpack):
        """Recursively moves down a component, finally returning a list of
         images and their offsets, given some already known pixel offset
         values."""
        image_location_list = []
        for sub_asset in self.parts:
            if sub_asset["type"] == "image":
                image_location_list = image_location_list+[(
                    assetpack.images[sub_asset["image_id"]],
                    sub_asset["x"]+offset_x,
                    sub_asset["y"]+offset_y
                )]
            else:
                sub_component = assetpack.components[sub_asset["component_id"]]
                sub_offset_x = sub_asset["x"]+offset_x
                sub_offset_y = sub_asset["y"]+offset_y
                new_ill = sub_component.get_image_location_list(
                                                          sub_offset_x,
                                                          sub_offset_y,
                                                          assetpack)
                image_location_list = image_location_list+new_ill
        return image_location_list

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Alters all the co-ordinates in a blueprint to match a new
         co-ordinate system."""
        for sub_asset in self.data["parts"]:
            sub_asset["x"] = sub_asset["x"] / scale_ratio_x
            sub_asset["y"] = sub_asset["y"] / scale_ratio_y


class ImageAsset:
    """A representation of an actual image file and the pixel offsets required
     to put it in the correct location."""
    def __init__(self, data, assetpack_name):
        self.assetpack_name = assetpack_name
        self.data = data
        self.name = data["name"]
        self.image_id = data["id"]
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
