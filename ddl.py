from PIL import Image
import json
import math

class ArtpackFactory:

    @staticmethod
    def fromFile(file):
        with open(file) as f:
            data = json.load(f)
            return Artpack(data)


class Artpack:
    def __init__(self, data):

        self.data = data
        self.assets = {}

        for asset in self.data['assets']:
            self.assets[asset['id']] = Asset(asset, self.data['grid'])

class Asset:
    def __init__(self, data, artpack_grid):
        self.data = data
        if "image" in self.data.keys():
            self.image = Image.open(self.data["image"])
        else:
            self.image = None
        if "grid" in self.data.keys():
            grid_definition = self.data["grid"]
        else:
            grid_definition = artpack_grid
        self.grid_type=grid_definition["type"]
        self.grid_square_pixel_width=grid_definition["width"]
        self.grid_square_pixel_height=grid_definition["height"]

        if self.image is None and "sub_assets" not in self.data.keys():
            raise Exception('Asset {} has no image or sub assets.',self.data["name"])

    def show(self):
        self.image.show()

    def get_sub_asset_location_isometric(self,x,y):
            pixel_x=(y*math.ceil(self.grid_square_pixel_width/2))-(x*math.floor(self.grid_square_pixel_width/2))
            pixel_y=(x*math.ceil(self.grid_square_pixel_height/2))+(y*math.floor(self.grid_square_pixel_height/2))
            return (pixel_x, pixel_y)

    def get_sub_asset_location_classic(self,x,y):
            pixel_x=x*self.grid_square_pixel_width
            pixel_y=y*self.grid_square_pixel_height
            return (pixel_x, pixel_y)

    def get_sub_assets(self, offset_x, offset_y, artpack):
        if self.image is not None:
            return [(self.data["id"], offset_x, offset_y)]
        else:
            sub_assets=[]
            for sub_asset in self.data["sub_assets"]:
                if self.grid_type=="isometric":
                    pixel_x, pixel_y = self.get_sub_asset_location_isometric(sub_asset["x"],sub_asset["y"])
                else:
                    pixel_x, pixel_y = self.get_sub_asset_location_classic(sub_asset["x"],sub_asset["y"])
                sub_assets=sub_assets+artpack.assets[sub_asset["asset_id"]].get_sub_assets(pixel_x,pixel_y,artpack)
            return sub_assets



class Map:
    def __init__(self, grid_definition, width=10, height=10):
        self.grid_width = width
        self.grid_height = height
        self.grid_square_pixel_width=grid_definition["width"]
        self.grid_square_pixel_height=grid_definition["height"]
        self.image_pixel_width = self.calculate_image_pixel_width()
        self.image_pixel_height = self.calculate_image_pixel_height()
        self.initialise_image(self.image_pixel_width, self.image_pixel_height)

    def calculate_image_pixel_width(self, width):
        return self.grid_width * self.grid_square_pixel_width

    def calculate_image_pixel_height(self, height):
        return self.grid_width * self.grid_square_pixel_height

    def initialise_image(self, width, height):
        self.image = Image.new('RGBA', (width, height),(255,0,0,0))

    def add_to_image(self, asset, x, y, dryrun=True):
        final_x=x-asset.data["top_left"]["x"]
        final_y=y-asset.data["top_left"]["y"]
        if not dryrun:
            self.image.paste(asset.image,(final_x,final_y),asset.image)
        else:
            return_image = self.image.copy()
            return_image.paste(asset.image,(final_x,final_y),asset.image)
            return_image.show()

    def render(self):
        self.image.show()


class IsometricMap(Map):

    def calculate_image_pixel_width(self):
        return math.ceil((self.grid_width*self.grid_square_pixel_width)/2+(self.grid_width*self.grid_square_pixel_width)/2)

    def calculate_image_pixel_height(self):
        return math.ceil((self.grid_height*self.grid_square_pixel_height)/2+(self.grid_height*self.grid_square_pixel_height)/2)

    def add_to_grid(self, asset, x, y, dryrun=True):
        centre_line=math.ceil((self.image_pixel_width-self.grid_square_pixel_width)/2)
        pixel_x=(y*math.ceil(self.grid_square_pixel_width/2))-(x*math.floor(self.grid_square_pixel_width/2))+centre_line
        pixel_y=(x*math.ceil(self.grid_square_pixel_height/2))+(y*math.floor(self.grid_square_pixel_height/2))
        self.add_to_image(asset, pixel_x, pixel_y, dryrun)


artpack = ArtpackFactory.fromFile('asset_definition.json')
floor = artpack.assets['floor_1x1_exact']
map = IsometricMap(artpack.data['grid'])
map.add_to_grid(floor,0,0,dryrun=False)
map.add_to_grid(floor,0,1,dryrun=False)

floor2=artpack.assets['floor_1x1_fuzzy']
map.add_to_grid(floor2,0,2,dryrun=False)
map.add_to_grid(floor2,1,1,dryrun=False)
map.render()
