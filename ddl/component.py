"""
Contains the Component class and ComponentFactory helper class
"""

import json


class Component:
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
