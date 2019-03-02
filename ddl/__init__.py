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
            self.blueprints[image['id']] = Blueprint(blueprint)


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

    def get_sub_assets(self, offset_x, offset_y, artpack, grid_square_pixel_width, grid_square_pixel_height):
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
