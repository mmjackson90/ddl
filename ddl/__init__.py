from PIL import Image
import json
import math

class ArtpackFactory:

    @staticmethod
    def load(name):
        with open('artpacks/' + name + '/artpack.json') as artpack_file, open('artpacks/' + name + '/imagepack.json') as imagepack_file:
            artpack = json.load(artpack_file)
            imagepack = json.load(imagepack_file)
            return Artpack(name, imagepack, artpack)


class Artpack:
    def __init__(self, name, imagepack, artpack):

        self.imagepack = imagepack
        self.images = {}
        self.blueprints = {}

        self.artpack = {
            'name': name,
            'grid': artpack['grid'],
            'blueprints': artpack['blueprints']
        }

        for image in self.imagepack['images']:
            self.images[image['id']] = Image_asset(image, artpack_name=name)

        for blueprint in self.artpack['blueprints']:
            self.blueprints[blueprint['id']] = Blueprint(blueprint)


class Image_asset:
    def __init__(self, data, artpack_name):
        self.data = data
        self.image = Image.open('artpacks/' + artpack_name + '/art/' + self.data["image"])


class Blueprint:
    def __init__(self, data):
        self.data = data
        if "sub_assets" not in self.data.keys():
            raise Exception('Blueprint {} has no sub assets.',self.data["name"])

    def show(self):
        self.image.show()

    def get_sub_asset_location_isometric(self,x,y,grid_square_pixel_width,grid_square_pixel_height):
            pixel_x=(y*math.ceil(grid_square_pixel_width/2))-(x*math.floor(grid_square_pixel_width/2))
            pixel_y=(x*math.ceil(grid_square_pixel_height/2))+(y*math.floor(grid_square_pixel_height/2))
            return (pixel_x, pixel_y)

    def get_sub_asset_location_classic(self,x,y,grid_square_pixel_width,grid_square_pixel_height):
            pixel_x=x*grid_square_pixel_width
            pixel_y=y*grid_square_pixel_height
            return (pixel_x, pixel_y)

    def get_sub_assets(self, offset_x, offset_y, artpack):
        grid_square_pixel_width=artpack.artpack['grid']['width']
        grid_square_pixel_height=artpack.artpack['grid']['height']
        image_location_list=[]
        for sub_asset in self.data["sub_assets"]:
            if self.data['grid_type']=="isometric":
                pixel_x, pixel_y = self.get_sub_asset_location_isometric(sub_asset["x"],sub_asset["y"], grid_square_pixel_width, grid_square_pixel_height)
            else:
                pixel_x, pixel_y = self.get_sub_asset_location_classic(sub_asset["x"],sub_asset["y"], grid_square_pixel_width, grid_square_pixel_height)
            if sub_asset["type"]=="image":
                image_location_list=image_location_list+[(artpack.images[sub_asset["image_id"]],pixel_x+offset_x,pixel_y+offset_y)]
            else:
                image_location_list=image_location_list+artpack.blueprints[sub_asset["blueprint_id"]].get_sub_assets(pixel_x+offset_x,pixel_y+offset_y,artpack)
        return image_location_list

class BlueprintFactory:
    def __init__(self, artpack, grid_type):
        self.artpack=artpack
        self.grid_type=grid_type
        self.current_asset=False
        self.id = None
        self.layer = None
        self.top_left = None
        self.name = None
        self.horizontally_flippable = None
        self.vertically_flippable = None
        self.tags = None
        self.connections = None
        self.sub_assets = None

    def new_blueprint(self, id, layer, top_left = (0, 0), name='',
    horizontally_flippable=True, vertically_flippable=True,
    tags=[],connections=[], sub_assets=[]):
        if self.current_asset:
            raise Exception('This factory is currently building another asset. Please finalise that asset before starting a new one.')
        self.current_asset=True
        self.id = id
        self.layer = layer
        self.top_left = top_left
        self.name = name
        self.horizontally_flippable = horizontally_flippable
        self.vertically_flippable = vertically_flippable
        self.tags = tags
        self.connections = connections
        self.sub_assets = sub_assets

    def add_image(self, image_id, x, y):
        if image_id not in self.artpack.images.keys():
            raise Exception('This image ID doesnt exist in this artpack.')
        sub_asset = {"type":"image", "image_id": image_id, "x": x, "y": y}
        self.sub_assets=self.sub_assets+[sub_asset]

    def add_blueprint(self, blueprint_id, x, y):
        if blueprint_id not in self.artpack.blueprints.keys():
            raise Exception('This blueprint ID doesnt exist in this artpack.')
        sub_asset = {"type":"blueprint", "blueprint_id": blueprint_id, "x": x, "y": y}
        self.sub_assets=self.sub_assets+[sub_asset]

    def get_blueprint(self):
        data = {
            "name": self.name,
            "id": self.id,
            "layer": self.layer,
            "grid_type":self.grid_type,
            "top_left": self.top_left,
            "sub_assets":self.sub_assets,
            "connections": self.connections,
            "horizontally_flippable": self.horizontally_flippable,
            "vertically_flippable": self.vertically_flippable,
            "tags": self.tags
        }
        return Blueprint(data)

    def clear_blueprint(self):
        self.current_asset=False
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
        image_list=self.get_blueprint()
        self.clear_blueprint()
        return image_list


class Renderer:
    def __init__(self, width=1000, height=1000, sub_assets=[]):
        self.image_pixel_width = width
        self.image_pixel_height = height
        self.sub_assets=sub_assets
        self.centre_line=round(width/2)
        self.initialise_image(self.image_pixel_width, self.image_pixel_height)

    def initialise_image(self, width, height):
        self.image = Image.new('RGBA', (width, height),(255,0,0,0))

    def add_sub_asset_list(self, sub_asset_list):
        self.sub_assets=sub_asset_list+self.sub_assets

    #This will need moving out to the asset factory, but for now leaving it here.
    def add_asset(self, asset, x, y, artpack):
        self.sub_assets=asset.get_sub_assets(x,y,artpack)+self.sub_assets

    def add_to_image(self, asset, x, y):
        final_x=x-asset.data["top_left"]["x"]
        final_y=y-asset.data["top_left"]["y"]
        self.image.paste(asset.image,(final_x,final_y),asset.image)

    def render(self):
        for asset, x, y in self.sub_assets:
            self.add_to_image(asset, x, y)
        self.image.show()
