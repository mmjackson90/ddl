"""
projection

Currently comes in two flavours (that are combined ATM).
Handles all co-ordinate transforms, image scaling operations and
conversion of co-ordinates to pixel offsets.
"""

import math


class Projection:
    """A class for storing information on and handling all transformations
     to/from another projection"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

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

    @staticmethod
    def get_image_offset(image, h_flip, v_flip):
        """Gets an image offset, bearing in mind flipping."""
        image_width, image_height = image.get_image_sizes()
        if not h_flip:
            image_offset_x = -image.top_left["x"]
        else:
            image_offset_x = -image_width+image.top_left["x"]
        if not v_flip:
            image_offset_y = -image.top_left["y"]
        else:
            image_offset_y = -image_height+image.top_left["y"]
        return (image_offset_x, image_offset_y)

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
        for info in image_location_list:
            image, x_coordinate, y_coordinate, h_flip, v_flip = info
            pixel_x, pixel_y = self.get_location_in_pixels(x_coordinate,
                                                           y_coordinate)

            image_offset_x, image_offset_y = self.get_image_offset(image,
                                                                   h_flip,
                                                                   v_flip)
            pixel_x = pixel_x+pixel_offset_x+image_offset_x
            pixel_y = pixel_y+pixel_offset_y+image_offset_y

            next_ipl = [(image, pixel_x, pixel_y, h_flip, v_flip)]
            image_pixel_list = image_pixel_list+next_ipl
        return image_pixel_list


class IsometricProjection(Projection):
    """An Isometric Projection subclass to overload how pixel offsets
     and get operations are treated."""
    def get_location_in_pixels(self, x_coordinate, y_coordinate):
        """Changes grid co-ordinates to pixels for an isometric grid"""
        pixel_x = (x_coordinate*math.ceil(self.width/2)) -\
                  (y_coordinate * math.floor(self.width/2))
        pixel_y = (x_coordinate*math.ceil(self.height/2)) +\
                  (y_coordinate*math.floor(self.height/2))
        return (round(pixel_x), round(pixel_y))


class TopDownProjection(Projection):
    """A TopDown Projection subclass to overload how pixel offsets
     and get operations are treated."""
    def get_location_in_pixels(self, x_coordinate, y_coordinate):
        """Changes grid co-ordinates to pixels for a classic cartesian grid"""
        pixel_x = x_coordinate*self.width
        pixel_y = y_coordinate*self.height
        return (round(pixel_x), round(pixel_y))
