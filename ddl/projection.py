"""
projection

Currently comes in two flavours (that are combined ATM).
Handles all co-ordinate transforms, image scaling operations and
conversion of co-ordinates to pixel offsets.
"""
from PIL import Image


class Projection:
    """A class for storing information on and handling all transformations
     to/from another projection"""
    def __init__(self, grid):
        self.type = grid["type"]
        self.height = grid["height"]
        self.width = grid["width"]

    def get_grid_ratios(self, desired_projection):
        size_ratio_x = desired_projection.width/self.width
        size_ratio_y = desired_projection.height/self.height
        return (size_ratio_x, size_ratio_y)

    def get_image_half_grid(self, desired_projection):
        if self.type == 'isometric':
            if self.width < desired_projection.width:
                half_grid_x = -desired_projection.width/2
            elif self.width > desired_projection.width:
                half_grid_x = +desired_projection.width/2
            else:
                half_grid_x = 0
        return (half_grid_x)

    def alter_grid_parameters(self, desired_projection):
        self.width = desired_projection.width
        self.height = desired_projection.height

    def resize_images(self, images, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
         images in the assetpack to match up the grids.
         Actually scales images at the moment, but could just change scale
         factors"""
        size_ratio_x, size_ratio_y = self.get_grid_ratios(desired_projection)
        for image in images.values():
            # Time to abuse python's referencing methods.
            # I hate that this still works.
            image.resize(size_ratio_x, size_ratio_y)

    def rescale_images(self, images, desired_projection):
        if self.type == "isometric":
            half_grid_x = self.get_image_half_grid(desired_projection)
            for image in images.values():
                image.rescale(half_grid_x)

    def rescale_components(self, components, desired_projection):
        scale_ratio_x, scale_ratio_y = self.get_grid_ratios(desired_projection)
        for component in components.values():
            component.rescale(scale_ratio_x, scale_ratio_y)
