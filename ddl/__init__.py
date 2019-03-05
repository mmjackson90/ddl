"""
Dungeon Description Language

Create all the functions currently in use by DDL.
Thus far this is only really the Artist code.
"""

from PIL import Image
import json
import math
from ddl.renderer import Renderer


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

        for image in imagepack['images']:
            self.images[image['id']] = ImageAsset(image, assetpack_name=name)

        for component in components_and_grid['components']:
            self.components[component['id']] = Component(component,
                                                         assetpack_name=name)

    def resize_images(self, desired_grid):
        """Accepts a desired grid size definition and uses it to rescale all
         images in the assetpack to match up the grids.
         Actually scales images at the moment, but could just change scale
         factors"""
        size_ratio_x = desired_grid['width']/self.grid['width']
        size_ratio_y = desired_grid['height']/self.grid['height']
        for image in self.images.values():
            # Time to abuse python's referencing methods
            image.resize(size_ratio_x, size_ratio_y)
        self.grid['width'] = desired_grid['width']
        self.grid['height'] = desired_grid['height']

    def rescale_pack(self, desired_grid):
        """Accepts a desired grid size definition and uses it to rescale all
        co-ordinates used in blueprints."""
        scale_ratio_x = self.grid['width']/desired_grid['width']
        scale_ratio_y = self.grid['height']/desired_grid['height']
        for component in self.components.values():
            component.rescale(scale_ratio_x, scale_ratio_y)
        if self.grid['type'] == 'isometric':
            if self.grid['width'] < desired_grid['width']:
                half_grid_x = -desired_grid['width']/2
            elif self.grid['width'] > desired_grid['width']:
                half_grid_x = +desired_grid['width']/2
            else:
                half_grid_x = 0
            for image in self.images.values():
                image.rescale(half_grid_x)
        self.grid['width'] = desired_grid['width']
        self.grid['height'] = desired_grid['height']


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

    def rescale(self, half_grid_x):
        """Alters the image top_left offsets to account for isometric grid"""
        self.top_left['x'] = round(self.top_left['x']+half_grid_x +
                                   self.image.width/2)

    def show(self):
        """Show the image."""
        self.image.show()


class Component:
    """This is a space saving measure that records
     multiple image_assets and components (collectively known as assets)
     and their respective positions within the Asset Pack's grid."""
    def __init__(self, data, assetpack_name):
        self.data = data
        # The assetpack this component is a part of
        self.assetpack_name = assetpack_name
        if "sub_assets" in data.keys():
            self.sub_assets = data["sub_assets"]
        else:
            raise Exception('Component {} has no sub assets.',
                            self.data["name"])

    def get_image_location_list(self, offset_x, offset_y, assetpack):
        """Recursively moves down a component, finally returning a list of
         images and their offsets, given some already known pixel offset
         values."""
        image_location_list = []
        for sub_asset in self.sub_assets:
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
        for sub_asset in self.data["sub_assets"]:
            sub_asset["x"] = sub_asset["x"] * scale_ratio_x
            sub_asset["y"] = sub_asset["y"] * scale_ratio_y


class ComponentFactory:
    """A class to help build componentss in-console.
    Needs to know an assetpack that it's using and co-ordinate information."""
    def __init__(self, assetpack, projection):
        self.assetpack = assetpack
        self.projection = projection
        self.clear_component()

    def change_assetpack(self, assetpack):
        """Checks a new assetpack can be used to build this component, then
         switches assetpack. Mostly used for A/B testing how components
         render"""
        for sub_asset in self.sub_assets:
            if sub_asset["type"] == "image":
                if sub_asset["image_id"] not in assetpack.images.keys():
                    raise Exception('Assetpack missing image %s',
                                    sub_asset["image_id"])
            if sub_asset["type"] == "component":
                if sub_asset["component_id"] not in\
                 assetpack.components.keys():
                    raise Exception('Assetpack missing component %s',
                                    sub_asset["component_id"])
        self.assetpack = assetpack

    def new_component(self, component_id, layer, top_left=(0, 0), name='',
                      horizontally_flippable=True, vertically_flippable=True,
                      tags=None, connections=None, sub_assets=None):
        """Initialises a new, empty component. All component parameters can
         be set using this method, so it's possible to 'copy' another component
        . Cannot be used twice if another component is under construction."""
        if self.current_component:
            raise Exception('''This factory is currently building another
 component. Please finalise that asset before starting a new one.''')
        self.current_component = True
        self.component_id = component_id
        self.layer = layer
        self.top_left = top_left
        self.name = name
        self.horizontally_flippable = horizontally_flippable
        self.vertically_flippable = vertically_flippable
        self.tags = [] if tags is None else tags
        self.connections = [] if connections is None else connections
        self.sub_assets = [] if sub_assets is None else sub_assets

    def add_image(self, image_id, x_coordinate, y_coordinate):
        """Adds a specific image asset to the component at grid co-ordinates
         x and y."""
        if image_id not in self.assetpack.images.keys():
            raise Exception('This image ID doesnt exist in this assetpack.')
        sub_asset = {"type": "image",
                     "image_id": image_id,
                     "x": x_coordinate,
                     "y": y_coordinate}
        self.sub_assets = self.sub_assets+[sub_asset]

    def add_component(self, component_id, x_coordinate, y_coordinate):
        """Adds a specific component to the component at grid co-ordinates
         x and y."""
        if component_id not in self.assetpack.components.keys():
            raise Exception('This component ID isn\'t in this assetpack.')
        sub_asset = {"type": "component",
                     "component_id": component_id,
                     "x": x_coordinate,
                     "y": y_coordinate}
        self.sub_assets = self.sub_assets+[sub_asset]

    def remove_last_sub_asset(self):
        """Removes the last sub asset (and therefore all it's sub assets)."""
        self.sub_assets.pop()

    def get_component(self):
        """Creates and returns the component without clearing the factory."""
        data = {
            "name": self.name,
            "id": self.component_id,
            "layer": self.layer,
            "projection": self.projection,
            "top_left": self.top_left,
            "sub_assets": self.sub_assets,
            "connections": self.connections,
            "horizontally_flippable": self.horizontally_flippable,
            "vertically_flippable": self.vertically_flippable,
            "tags": self.tags
        }
        return Component(data, self.assetpack.name)

    def clear_component(self):
        """Clears the factory to begin building a new component."""
        self.current_component = False
        self.id = None
        self.layer = None
        self.top_left = None
        self.name = None
        self.horizontally_flippable = None
        self.vertically_flippable = None
        self.tags = None
        self.connections = None
        self.sub_assets = None

    def pull_component(self):
        """Creates and returns the component and clears the factory"""
        image_list = self.get_component()
        self.clear_component()
        return image_list

    def output_component(self, destination='screen', filename=None):
        """Sets up a locator and a renderer and renders the current component.
         Can take many shortcuts as it knows it's own assetpack/grid.
         Defaults to screen output, but can throw to file if needed."""
        positioner = Positioner(self.assetpack.grid)
        image_location_list = self.get_component()\
                                  .get_image_location_list(0, 0,
                                                           self.assetpack)
        image_list = positioner.get_image_pixel_list(0, 0, image_location_list)
        Renderer(image_list).output(destination, filename)


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
    def get_locations_isometric(x_coordinate, y_coordinate,
                                grid_square_pixel_width,
                                grid_square_pixel_height):
        """Changes grid co-ordinates to pixels for an isometric grid"""
        pixel_x = (y_coordinate*math.ceil(grid_square_pixel_width/2)) -\
                  (x_coordinate * math.floor(grid_square_pixel_width/2))
        pixel_y = (x_coordinate*math.ceil(grid_square_pixel_height/2)) +\
                  (y_coordinate*math.floor(grid_square_pixel_height/2))
        return (round(pixel_x), round(pixel_y))

    @staticmethod
    def get_locations_classic(x_coordinate, y_coordinate,
                              grid_square_pixel_width,
                              grid_square_pixel_height):
        """Changes grid co-ordinates to pixels for a classic cartesian grid"""
        pixel_x = x_coordinate*grid_square_pixel_width
        pixel_y = y_coordinate*grid_square_pixel_height
        return (round(pixel_x), round(pixel_y))

    def get_image_pixel_list(self,
                             grid_offset_x,
                             grid_offset_y,
                             image_location_list):
        """Goes through a list of images and grid co-ordinates and returns a
         list of images and pixel co-ordinates."""
        # Worry about performance later.
        grid_width = self.grid_definition['width']
        grid_height = self.grid_definition['height']
        pixel_offsets = self.get_location_in_pixels(grid_offset_x,
                                                    grid_offset_y,
                                                    grid_width,
                                                    grid_height)
        pixel_offset_x, pixel_offset_y = pixel_offsets
        image_pixel_list = []
        for image, x_coordinate, y_coordinate in image_location_list:
            pixel_x, pixel_y = self.get_location_in_pixels(x_coordinate,
                                                           y_coordinate,
                                                           grid_width,
                                                           grid_height)
            pixel_x = pixel_x+pixel_offset_x
            pixel_y = pixel_y+pixel_offset_y
            image_pixel_list = image_pixel_list+[(image, pixel_x, pixel_y)]
        return image_pixel_list
