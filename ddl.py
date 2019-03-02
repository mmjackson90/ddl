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
            #This should return a reference to the correct asset and x/y
            return [(artpack.assets[self.data["id"]], offset_x, offset_y)]
        else:
            sub_assets=[]
            for sub_asset in self.data["sub_assets"]:
                if self.grid_type=="isometric":
                    pixel_x, pixel_y = self.get_sub_asset_location_isometric(sub_asset["x"],sub_asset["y"])
                else:
                    pixel_x, pixel_y = self.get_sub_asset_location_classic(sub_asset["x"],sub_asset["y"])
                sub_assets=sub_assets+artpack.assets[sub_asset["asset_id"]].get_sub_assets(pixel_x+offset_x,pixel_y+offset_y,artpack)
            return sub_assets



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


artpack = ArtpackFactory.fromFile('asset_definition.json')
floor = artpack.assets['floor_1x1_exact']
floor2 = artpack.assets['floor_1x1_fuzzy']
floor3 = artpack.assets['floor_2x2_exact']
renderer = Renderer()
renderer.add_asset(floor3,500,0,artpack)
renderer.render()
