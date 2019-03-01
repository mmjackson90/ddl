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
            self.assets[asset['id']] = Asset(asset)

class Asset:
    def __init__(self, data):
        self.data = data
        self.image = Image.open(self.data["image"])

    def show(self):
        self.image.show()

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
        if not dryrun:
            self.image.paste(asset.image,(x,y),asset.image)
        else:
            return_image = self.image.copy()
            return_image.paste(asset.image,(x,y),asset.image)
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
floor = artpack.assets['stone_floor_1x1']
map = IsometricMap(artpack.data['grid'])
map.add_to_grid(floor,0,0,dryrun=False)
map.add_to_grid(floor,0,1,dryrun=False)
map.render()
