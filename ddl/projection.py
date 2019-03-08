"""
projection

Currently comes in two flavours (that are combined ATM).
Handles all co-ordinate transforms, image scaling operations and
conversion of co-ordinates to pixel offsets.
"""
from PIL import Image
import math


class Projection:
    """A class for storing information on and handling all transformations
     to/from another projection"""
    def __init__(self, grid):
        self.type = grid["type"]
        self.height = grid["height"]
        self.width = grid["width"]

    def get_grid_ratios(self, desired_projection):
        """Get the width/height ratios to convert one projection to another"""
        size_ratio_x = desired_projection.width/self.width
        size_ratio_y = desired_projection.height/self.height
        return (size_ratio_x, size_ratio_y)

    def alter_grid_parameters(self, desired_projection):
        """Alters this projection's width and height. Cannot alter type"""
        self.width = desired_projection.width
        self.height = desired_projection.height

    def resize_images(self, images, desired_projection):
        """Accepts a desired grid size definition and uses it to resize all
         images passed in as a dict.
         Actually scales images at the moment, but could just change scale
         factors"""
        size_ratio_x, size_ratio_y = self.get_grid_ratios(desired_projection)
        for image in images.values():
            # Time to abuse python's referencing methods.
            # I hate that this still works.
            image.resize(size_ratio_x, size_ratio_y)

    def rescale_components(self, components, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
         components passed in as a dict."""
        scale_ratio_x, scale_ratio_y = self.get_grid_ratios(desired_projection)
        for component in components.values():
            component.rescale(scale_ratio_x, scale_ratio_y)

    def get_image_pixel_list(self,
                             grid_offset_x,
                             grid_offset_y,
                             image_location_list):
        """Goes through a list of images and grid co-ordinates and returns a
         list of images and pixel co-ordinates."""
        # Worry about performance later.
        pixel_offsets = self.get_location_in_pixels(grid_offset_x,
                                                    grid_offset_y)
        pixel_offset_x, pixel_offset_y = pixel_offsets
        image_pixel_list = []
        for image, x_coordinate, y_coordinate in image_location_list:
            pixel_x, pixel_y = self.get_location_in_pixels(x_coordinate,
                                                           y_coordinate)
            pixel_x = pixel_x+pixel_offset_x
            pixel_y = pixel_y+pixel_offset_y
            image_pixel_list = image_pixel_list+[(image, pixel_x, pixel_y)]
        return image_pixel_list


class IsometricProjection(Projection):
    """An Isometric Projection subclass to overload how pixel offsets
     and get operations are treated."""
    def get_location_in_pixels(self, x_coordinate, y_coordinate):
        """Changes grid co-ordinates to pixels for an isometric grid"""
        pixel_x = (y_coordinate*math.ceil(self.width/2)) -\
                  (x_coordinate * math.floor(self.width/2))
        pixel_y = (x_coordinate*math.ceil(self.height/2)) +\
                  (y_coordinate*math.floor(self.height/2))
        return (round(pixel_x), round(pixel_y))

    def get_image_half_grid(self, desired_projection):
        """Gets the offset required to make all images in the current
        projection match the grid of the desired projection"""
        half_grid_x = (self.width-desired_projection.width)/2
        return (half_grid_x)

    def rescale_images(self, images, desired_projection):
        """Accepts a desired grid size definition and uses it to rescale all
         images passed in as a dict."""
        for image in images.values():
            image.rescale(self.get_image_half_grid(desired_projection))


class TopDownProjection(Projection):
    def get_location_in_pixels(x_coordinate, y_coordinate):
        """Changes grid co-ordinates to pixels for a classic cartesian grid"""
        pixel_x = x_coordinate*self.width
        pixel_y = y_coordinate*self.height
        return (round(pixel_x), round(pixel_y))

    def rescale_images(self, images, desired_projection):
        """Accepts a desired grid size definition and does nothing with it,
        This only exists because Isometric grids are complicated."""
        pass
