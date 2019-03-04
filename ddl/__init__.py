"""Create all the functions currently in use by DDL. \
Thus far this is only really the Artist code."""


from PIL import Image
import json
import math


class ArtpackFactory:
    """A factory for creating AssetPacks"""
    @staticmethod
    def load(name):
        """Loads AssetPacks from their Art and Image packs,
         given an appropriate name"""
        with open(
                'assetpacks/' + name + '/blueprints.json'
                ) as artpack_file, open(
                'assetpacks/' + name + '/images.json'
                ) as imagepack_file:
            artpack = json.load(artpack_file)
            imagepack = json.load(imagepack_file)
            return Artpack(name, imagepack, artpack)


class Artpack:
    """Really an Assetpack. This class records all information needed to
     position and render the various images located in an artpack.
     Please see the artpack and imagepack schema for more info"""
    def __init__(self, name, imagepack, artpack):

        self.imagepack = imagepack
        self.images = {}
        self.blueprints = {}

        self.artpack = {
            'name': name,
            'grid': artpack['grid'],
        }

        for image in self.imagepack['images']:
            self.images[image['id']] = Image_asset(image, artpack_name=name)

        for blueprint in artpack['blueprints']:
            self.blueprints[blueprint['id']] = Blueprint(blueprint,
                                                         artpack_name=name)

    def resize_images(self, desired_grid):
        """Accepts a desired grid size definition and uses it to resize all
         images in the artpack to match up the grids.
         Actually resizes images at the moment, but could just change size
         factors"""
        size_ratio_x = desired_grid['width']/self.artpack['grid']['width']
        size_ratio_y = desired_grid['height']/self.artpack['grid']['height']
        for image in self.images.values():
            # Time to abuse python's referencing methods
            image.resize(size_ratio_x, size_ratio_y)
        self.artpack['grid']['width'] = desired_grid['width']
        self.artpack['grid']['height'] = desired_grid['height']

    def rescale_components(self, desired_grid):
        """Accepts a desired grid size definition and uses it to rescale all
        co-ordinates used in blueprints."""
        scale_ratio_x = self.artpack['grid']['width']/desired_grid['width']
        scale_ratio_y = self.artpack['grid']['height']/desired_grid['height']
        for blueprint in self.blueprints.values():
            blueprint.rescale(scale_ratio_x, scale_ratio_y)
        self.artpack['grid']['width'] = desired_grid['width']
        self.artpack['grid']['height'] = desired_grid['height']


class Image_asset:
    """A representation of an actual image file and the pixel offsets required
     to put it in the correct location."""
    def __init__(self, data, artpack_name):
        self.artpack_name = artpack_name
        self.data = data
        self.image = Image.open('assetpacks/' + artpack_name + '/art/' +
                                self.data["image"])

    def resize(self, size_ratio_x, size_ratio_y):
        """Alters the image and it's top_left pixel offsets by some x and y
         scale factors"""
        final_image_width = round(self.image.width*size_ratio_x)
        final_image_height = round(self.image.height*size_ratio_y)
        self.image = self.image.resize((final_image_width, final_image_height))
        self.data['top_left']['x'] = round(self.data['top_left']['x'] *
                                           size_ratio_x)
        self.data['top_left']['y'] = round(self.data['top_left']['y'] *
                                           size_ratio_y)

    def show(self):
        """Show the image."""
        self.image.show()


class Blueprint:
    """Soon to be called component: This is a space saving measure that records
     multiple blueprints and components and their respective positions within
     the Asset Pack's grid. Like an image it too can have a pixel offset
     but it shouldnt really need it."""
    # TODO: Not sure component top_left pixel offsets are currently in place
    def __init__(self, data, artpack_name):
        self.data = data
        # The artpack this blueprint is a part of
        self.artpack_name = artpack_name
        if "sub_assets" not in self.data.keys():
            raise Exception('Blueprint {} has no sub assets.',
                            self.data["name"])

    def get_image_location_list(self, offset_x, offset_y, artpack):
        """Recursively moves down a blueprint, finally returning a list of
         images and their offsets, given some already known pixel offset
         values."""
        image_location_list = []
        for sub_asset in self.data["sub_assets"]:
            if sub_asset["type"] == "image":
                image_location_list = image_location_list+[(
                    artpack.images[sub_asset["image_id"]],
                    sub_asset["x"]+offset_x,
                    sub_asset["y"]+offset_y
                )]
            else:
                sub_blueprint = artpack.blueprints[sub_asset["blueprint_id"]]
                sub_offset_x = sub_asset["x"]+offset_x
                sub_offset_y = sub_asset["y"]+offset_y
                new_ill = sub_blueprint.get_image_location_list(
                                                          sub_offset_x,
                                                          sub_offset_y,
                                                          artpack)
                image_location_list = image_location_list+new_ill
        return image_location_list

    def rescale(self, scale_ratio_x, scale_ratio_y):
        """Alters all the co-ordinates in a blueprint to match a new
         co-ordinate system."""
        for sub_asset in self.data["sub_assets"]:
            sub_asset["x"] = sub_asset["x"] * scale_ratio_x
            sub_asset["y"] = sub_asset["y"] * scale_ratio_y


class BlueprintFactory:
    """A class to help build blueprints in-console.
    Needs to know an assetpack that it's using and co-ordinate information."""
    def __init__(self, artpack, projection):
        self.artpack = artpack
        self.projection = projection
        self.clear_blueprint()

    def new_blueprint(self, id, layer, top_left=(0, 0), name='',
                      horizontally_flippable=True, vertically_flippable=True,
                      tags=None, connections=None, sub_assets=None):
        """Initialises a new, empty blueprint. All blueprint parameters can
         be set using this method, so it's possible to 'copy' another blueprint
        . Cannot be used twice if another blueprint is under construction."""
        if self.current_asset:
            raise Exception('''This factory is currently building another
 blueprint. Please finalise that asset before starting a new one.''')
        self.current_asset = True
        self.id = id
        self.layer = layer
        self.top_left = top_left
        self.name = name
        self.horizontally_flippable = horizontally_flippable
        self.vertically_flippable = vertically_flippable
        self.tags = [] if tags is None else tags
        self.connections = [] if connections is None else connections
        self.sub_assets = [] if sub_assets is None else sub_assets

    def add_image(self, image_id, x, y):
        """Adds a specific image asset to the blueprint at grid co-ordinates
         x and y."""
        if image_id not in self.artpack.images.keys():
            raise Exception('This image ID doesnt exist in this artpack.')
        sub_asset = {"type": "image", "image_id": image_id, "x": x, "y": y}
        self.sub_assets = self.sub_assets+[sub_asset]

    def add_blueprint(self, blueprint_id, x, y):
        """Adds a specific blueprint to the blueprint at grid co-ordinates
         x and y."""
        if blueprint_id not in self.artpack.blueprints.keys():
            raise Exception('This blueprint ID doesnt exist in this artpack.')
        sub_asset = {"type": "blueprint",
                     "blueprint_id": blueprint_id,
                     "x": x,
                     "y": y}
        self.sub_assets = self.sub_assets+[sub_asset]

    def get_blueprint(self):
        """Creates and returns the blueprint without clearing the factory."""
        data = {
            "name": self.name,
            "id": self.id,
            "layer": self.layer,
            "projection": self.projection,
            "top_left": self.top_left,
            "sub_assets": self.sub_assets,
            "connections": self.connections,
            "horizontally_flippable": self.horizontally_flippable,
            "vertically_flippable": self.vertically_flippable,
            "tags": self.tags
        }
        return Blueprint(data, self.artpack.artpack['name'])

    def clear_blueprint(self):
        """Clears the factory to begin building a new blueprint."""
        self.current_asset = False
        self.id = None
        self.layer = None
        self.top_left = None
        self.name = None
        self.horizontally_flippable = None
        self.vertically_flippable = None
        self.tags = None
        self.connections = None
        self.sub_assets = None

    def pull_blueprint(self):
        """Creates and returns the blueprint and clears the factory"""
        image_list = self.get_blueprint()
        self.clear_blueprint()
        return image_list


class Positioner:
    """Responsible for getting a list of images and grid co-ordinates and
     turning it into a list of images and pixel co-ordinates, given the grid
     definition it is initialised with."""
    def __init__(self, grid_definition):
        self.grid_definition = grid_definition
        # MONKEYPAAAAAAAAAAAAAAATCH!!! (I think it's neater here,
        # given that we know the co-ordinate system.
        if grid_definition['type'] == "isometric":
            self.get_location_in_pixels = self.get_locations_isometric
        else:
            self.get_location_in_pixels = self.get_locations_classic

    @staticmethod
    def get_locations_isometric(x, y,
                                grid_square_pixel_width,
                                grid_square_pixel_height):
        """Changes grid co-ordinates to pixels for an isometric grid"""
        pixel_x = (y*math.ceil(grid_square_pixel_width/2))-(x*math.floor(
            grid_square_pixel_width/2))
        pixel_y = (x*math.ceil(grid_square_pixel_height/2))+(y*math.floor(
            grid_square_pixel_height/2))
        return (round(pixel_x), round(pixel_y))

    @staticmethod
    def get_locations_classic(x, y,
                              grid_square_pixel_width,
                              grid_square_pixel_height):
        """Changes grid co-ordinates to pixels for a classic cartesian grid"""
        pixel_x = x*grid_square_pixel_width
        pixel_y = y*grid_square_pixel_height
        return (round(pixel_x), round(pixel_y))

    def get_image_pixel_list(self,
                             pixel_offset_x,
                             pixel_offset_y,
                             image_location_list):
        """Goes through a list of images and grid co-ordinates and returns a
         list of images and pixel co-ordinates."""
        # Worry about performance later.
        image_pixel_list = []
        for image, x, y in image_location_list:
            grid_width = self.grid_definition['width']
            grid_height = self.grid_definition['height']
            pixel_x, pixel_y = self.get_location_in_pixels(x, y,
                                                           grid_width,
                                                           grid_height)
            pixel_x = pixel_x+pixel_offset_x
            pixel_y = pixel_y+pixel_offset_y
            image_pixel_list = image_pixel_list+[(image, pixel_x, pixel_y)]
        return image_pixel_list


class Renderer:
    """This class renders lists of images and their pixel locations."""
    def __init__(self, width=1000, height=1000, image_pixel_list=None):
        self.image_pixel_width = width
        self.image_pixel_height = height
        if image_pixel_list is None:
            self.image_pixel_list = []
        else:
            self.image_pixel_list = image_pixel_list
        self.centre_line = round(width/2)
        self.initialise_image(self.image_pixel_width, self.image_pixel_height)

    def initialise_image(self, width, height):
        """Set up a clean image"""
        self.image = Image.new('RGBA', (width, height), (255, 0, 0, 0))

    def add_image_pixel_list(self, image_pixel_list):
        """Add some images at some series of offsets to the list of images to
         be rendered"""
        self.image_pixel_list = image_pixel_list+self.image_pixel_list

    def add_to_image(self, asset, x, y):
        """Adds all images to the final picture, taking into account their
         top-left corner offsets"""
        final_x = x-asset.data["top_left"]["x"]
        final_y = y-asset.data["top_left"]["y"]
        self.image.paste(asset.image, (final_x, final_y), asset.image)

    def render(self):
        """Add all images in the list to the final image and show it."""
        for asset, x, y in self.image_pixel_list:
            self.add_to_image(asset, x, y)
        self.image.show()
