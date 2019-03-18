"""
Contains the Imageasset and ComponentAsset classes, along with the Asset
superclass.
"""

from PIL import Image
from json import dumps
from copy import deepcopy


class Asset:
    """
    The superclass for components and images. Implements methods common to
    both to allow for easier implementation of global asset lists.
    """
    def __init__(self, data, assetpack_id):
        self.data = data
        self.assetpack_id = assetpack_id
        self.name = data['name']
        self.asset_id = data['id']

    def get_full_id(self):
        """ Return the full ID of this asset, including the Assetpack ID"""
        return (self.assetpack_id + '.' + self.asset_id)

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Passes. Implementations of this method exists in subclasses"""
        pass

    def resize(self, size_ratio_x, size_ratio_y):
        """Passes. Implementations of this method exists in subclasses"""
        pass

    def reset_sub_parts(self):
        """Passes. Implementations of this method exists in subclasses"""
        pass


class ComponentAsset(Asset):
    """This is a space saving measure that records
     multiple image_assets and components (collectively known as assets)
     and their respective positions within the Asset Pack's grid."""
    def __init__(self, data, assetpack):
        super().__init__(data, assetpack.pack_id)
        self.assetpack = assetpack
        if "parts" in data.keys():
            self.parts = data["parts"]

            self.parts_instantiated = False
            self.reset_sub_parts()
        else:
            raise Exception('Component {} has no parts.',
                            self.data["name"])
        self.tags = data["tags"]

    def reset_sub_parts(self):
        """Sets the ID of any sub parts to be the full_id of the part"""
        for sub_part in self.parts:
            sub_part["asset_id"] = self.get_part_full_id(sub_part)

    def instantiate_sub_parts(self):
        i = 0
        self.part_pointers = [None]*len(self.parts)
        for sub_part in self.parts:
            if sub_part['type'] == "image":
                sub_image = self.assetpack.images[sub_part['asset_id']]
                self.part_pointers[i] = (sub_image, sub_part["x"], sub_part["y"])
            else:
                sub_component = self.assetpack.components[sub_part['asset_id']]
                self.part_pointers[i] = (sub_component, sub_part["x"], sub_part["y"])
            i = i + 1
        self.parts_instantiated = True

    def get_image_location_list(self, offset_x, offset_y):
        """
        For a given component, recurses down it's tree of parts until we end
        up with nothing but a list of images and their absolute (by grid)
        offsets
        """
        if not self.parts_instantiated:
            self.instantiate_sub_parts()

        image_location_list = []
        for part in self.part_pointers:
            asset, part_x, part_y = part
            part_offset_x = part_x+offset_x
            part_offset_y = part_y+offset_y
            if isinstance(asset, ComponentAsset):
                image_location_list = image_location_list + asset.\
                    get_image_location_list(part_offset_x, part_offset_y)
            else:
                image_location_list = image_location_list + [(asset,
                                                              part_offset_x,
                                                              part_offset_y)]
        return image_location_list

    def get_part_full_id(self, sub_part):
        """Gives the correct part id, given the assetpack."""
        if sub_part['type'] == 'image':
            # Naive check to see if this already has an assetpack name
            if len(sub_part["image_id"].split('.')) != 2:
                return(self.assetpack_id + '.' + sub_part["image_id"])
            else:
                return(sub_part["image_id"])
        else:
            if len(sub_part["component_id"].split('.')) != 2:
                return(self.assetpack_id + '.' + sub_part["component_id"])
            else:
                return(sub_part["component_id"])

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Alters all the co-ordinates in a blueprint to match a new
         co-ordinate system."""
        for sub_asset in self.data["parts"]:
            sub_asset["x"] = sub_asset["x"] / scale_ratio_x
            sub_asset["y"] = sub_asset["y"] / scale_ratio_y

    def add_image(self, image, x_coordinate, y_coordinate):
        """Adds a specific image asset to the component at grid co-ordinates
         x and y."""
        sub_asset = {"type": "image",
                     "image_id": image.asset_id,
                     "x": x_coordinate,
                     "y": y_coordinate,
                     "asset_id": image.get_full_id()}
        self.parts = self.parts+[sub_asset]

    def add_component(self, component, x_coordinate, y_coordinate):
        """Adds a specific component to the component at grid co-ordinates
         x and y."""
        sub_asset = {"type": "component",
                     "component_id": component.asset_id,
                     "x": x_coordinate,
                     "y": y_coordinate,
                     "asset_id": component.get_full_id()}
        self.parts = self.parts+[sub_asset]

    def remove_last_part(self):
        """Removes the last part (and therefore all it's sub-parts)."""
        self.parts.pop()

    def get_data(self):
        """Creates the original component data to either return or print."""
        parts = deepcopy(self.parts)
        for part in parts:
            part.pop('asset_id', None)
        return {
            "name": self.name,
            "id": self.asset_id,
            "parts": parts,
            "tags": self.tags
        }

    def get_json(self):
        """Prints the component in json"""
        return(dumps(self.get_data(), indent=4))


class ImageAsset(Asset):
    """A representation of an actual image file and the pixel offsets required
     to put it in the correct location."""
    def __init__(self, data, assetpack_id, assetpack_path):
        super().__init__(data, assetpack_id)
        if "top_left" in data.keys():
            self.top_left = data["top_left"]
        else:
            self.top_left = {"x": 0, "y": 0}

        self.image = Image.open(assetpack_path + '/art/' +
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
