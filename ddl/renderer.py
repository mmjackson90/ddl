"""
Renderer

Handle assembling an output image, any chrome, and displaying/saving
accordingly.
"""

import random
import string

from PIL import Image


class Renderer:
    """This class renders lists of images and their pixel locations."""
    def __init__(self, image_pixel_list=None):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.image_pixel_list = []
        if image_pixel_list is not None:
            self.add_image_pixel_list(image_pixel_list)

    def initialise_image(self, width, height):
        """Set up a clean image"""
        self.image = Image.new('RGBA', (width, height), (255, 0, 0, 0))

    def add_image_pixel_list(self, image_pixel_list):
        """Add some images at some series of offsets to the list of images to
         be rendered"""
        for info in image_pixel_list:
            sub_image, pixel_x, pixel_y = info[:3]
            min_x, min_y, max_x, max_y = \
                self.get_image_pixel_boundaries(sub_image, pixel_x, pixel_y)
            self.min_x = min(min_x, self.min_x)
            self.min_y = min(min_y, self.min_y)
            self.max_x = max(max_x, self.max_x)
            self.max_y = max(max_y, self.max_y)

        self.image_pixel_list = image_pixel_list+self.image_pixel_list

    def add_to_image(self, sub_image, pixel_x, pixel_y, h_flip, v_flip):
        """Adds all images to the final picture, taking into account their
         top-left corner offsets"""
        final_x = pixel_x
        final_y = pixel_y
        # second image.image call is alpha mask.
        image = sub_image.get_image(h_flip, v_flip)
        self.image.paste(image, (final_x, final_y), image)

    @staticmethod
    def get_image_pixel_boundaries(sub_image, pixel_x, pixel_y):
        """Get the pixel boundaries, given all the images."""
        image_width, image_height = sub_image.get_image_sizes()
        min_x = pixel_x
        min_y = pixel_y
        max_x = min_x+image_width
        max_y = min_y+image_height
        return (min_x, min_y, max_x, max_y)

    def assemble(self):
        """Add all images in the list to the final image."""
        image_pixel_width = self.max_x - self.min_x + 20
        image_pixel_height = self.max_y - self.min_y + 20
        self.initialise_image(image_pixel_width, image_pixel_height)
        for info in self.image_pixel_list:
            sub_image, pixel_x, pixel_y, h_flip, v_flip = info
            self.add_to_image(sub_image,
                              pixel_x-self.min_x+10,
                              pixel_y-self.min_y+10,
                              h_flip,
                              v_flip)

    def output(self, destination, filepath=None):
        """Actually put the image somewhere"""

        self.assemble()

        if destination == 'screen':
            self.image.show()
        elif destination == 'file':
            if not filepath:
                filepath = 'output/' + ''.join([random.SystemRandom()
                                                .choice(string.ascii_lowercase)
                                                for n in range(8)]) + ".png"
            self.image.save(filepath, "PNG")
        elif destination == 'variable':
            return self.image
        elif destination == 'dryrun':
            # This doesn't actually do anything, but is handy for testing there
            # are no material errors.
            return
        else:
            raise ValueError("Invalid output destination '{}'"
                             .format(destination))
