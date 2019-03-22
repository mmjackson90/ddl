"""Tests the renderer, just the renderer and nothing but the renderer"""
from pytest import raises
from PIL import Image
from ddl.renderer import Renderer


def test_init_with_ipl(monkeypatch):
    """Tests initialising with or without an image list calls the right functions"""
    fake_ipl = ['not', 'a', 'real', 'list']

    def fake_add_ipl(self, image_pixel_list):
        """Adds a fake Image Pixel List to an object"""
        self.image_pixel_list = image_pixel_list
    monkeypatch.setattr(Renderer, "add_image_pixel_list", fake_add_ipl)
    renderer = Renderer(fake_ipl)
    assert renderer.image_pixel_list == fake_ipl
    renderer2 = Renderer()
    assert renderer2.image_pixel_list == []


def test_initialise_image():
    """tests initialising a blank image"""
    renderer = Renderer()
    renderer.initialise_image(20, 10)
    assert isinstance(renderer.image, Image.Image)
    assert renderer.image.width == 20
    assert renderer.image.height == 10


def test_add_ipl(monkeypatch):
    """tests addin an image pixel list"""
    fake_ipl = [('image', -5, 20), ('image', 12, 3)]

    def fake_get_image_boundaries(sub_image, pixel_x, pixel_y):
        """Just returns image boundaries as though the image were 10x10"""
        assert sub_image == 'image'
        return (pixel_x, pixel_y, pixel_x+10, pixel_y+10)
    monkeypatch.setattr(Renderer, "get_image_pixel_boundaries",
                        staticmethod(fake_get_image_boundaries))
    renderer = Renderer()
    renderer.add_image_pixel_list(fake_ipl)
    assert renderer.min_x == -5
    assert renderer.max_x == 22
    assert renderer.min_y == 0
    assert renderer.max_y == 30


def test_add_to_image():
    """Tests the add to image method"""
    class FakeImage:
        """A fake image class"""
        def __init__(self, top_left, image):
            self.image = image
            self.top_left = top_left
            self.paste_called = False

        def paste(self, image, coord, mask):
            """Hides asserts inside a fake class. I like this pattern"""
            assert image == 'image_to_paste'
            assert coord == (2, 4)
            assert mask == 'image_to_paste'
            self.paste_called = True

    renderer = Renderer()
    image_1 = FakeImage({}, 'image')
    image_2 = FakeImage({"x": 1, "y": 2}, 'image_to_paste')
    renderer.image = image_1
    renderer.add_to_image(image_2, 3, 6)
    assert renderer.image.paste_called


def test_get_image_pixel_boundaries():
    """Tests the image pixel boundaries are returned correctly"""
    class VarStorage:
        """ A fake class to store things"""
    class FakeImage:
        """A fake image class"""
        def __init__(self):
            self.top_left = {"x": 1, "y": 2}
            self.image = VarStorage()
            self.image.width = 10
            self.image.height = 20
    image = FakeImage()
    min_x, min_y, max_x, max_y = Renderer.get_image_pixel_boundaries(image, 3, 5)
    assert min_x == 2
    assert min_y == 3
    assert max_x == 12
    assert max_y == 23


def test_assemble(monkeypatch):
    """Tests image assembly calls are made correctly"""
    class VarStorage:
        """ A fake class to store things"""
    def fake_initialise(self, width, height):
        """Monkeypatch out the initialise function"""
        self.test_variables = VarStorage()
        self.test_variables.sub_images = []
        self.test_variables.pixel_xs = []
        self.test_variables.pixel_ys = []
        assert width == 30
        assert height == 40

    def fake_add_to_image(self, sub_image, pixel_x, pixel_y):
        """Monkeypatch out the add to image function"""
        self.test_variables.sub_images.append(sub_image)
        self.test_variables.pixel_xs.append(pixel_x)
        self.test_variables.pixel_ys.append(pixel_y)

    monkeypatch.setattr(Renderer, "initialise_image", fake_initialise)
    monkeypatch.setattr(Renderer, "add_to_image", fake_add_to_image)
    renderer = Renderer()
    renderer.max_x = 60
    renderer.min_x = 50
    renderer.max_y = 60
    renderer.min_y = 40
    renderer.image_pixel_list = [('image1', 1, 2), ('image2', 3, 5)]
    renderer.assemble()
    assert renderer.test_variables.sub_images == ['image1', 'image2']
    assert renderer.test_variables.pixel_xs == [-39, -37]
    assert renderer.test_variables.pixel_ys == [-28, -25]


class OutputFakeImage:
    """A fake image to store various output stats."""
    def __init__(self):
        self.shown = False
        self.save_filepath = ''
        self.image = 'image'

    def show(self):
        """Sets the shown flag"""
        self.shown = True

    def save(self, filepath, type_of_image):
        """quick assert and saves the filepath"""
        assert type_of_image == 'PNG'
        self.save_filepath = filepath


def fake_assemble(self):
    """A fake assemble function"""
    self.image = OutputFakeImage()


def test_output_screen(monkeypatch):
    """Tests the output logic works"""
    monkeypatch.setattr(Renderer, "assemble", fake_assemble)
    renderer = Renderer()
    assert renderer.output('screen') is None
    assert renderer.image.shown


def test_output_file(monkeypatch):
    """Tests the output logic works"""
    monkeypatch.setattr(Renderer, "assemble", fake_assemble)
    renderer = Renderer()
    assert renderer.output('file') is None
    assert renderer.image.save_filepath.split('/')[0] == 'output'
    assert len(renderer.image.save_filepath) == 19
    assert renderer.image.save_filepath.split('.')[-1] == 'png'


def test_output_variable(monkeypatch):
    """Tests the output logic works"""
    monkeypatch.setattr(Renderer, "assemble", fake_assemble)
    renderer = Renderer()
    assert isinstance(renderer.output('variable'), OutputFakeImage)


def test_output_dryrun(monkeypatch):
    """Tests the output logic works"""
    monkeypatch.setattr(Renderer, "assemble", fake_assemble)
    renderer = Renderer()
    assert renderer.output('dryrun') is None


def test_output_fail(monkeypatch):
    """Tests the output logic works"""
    monkeypatch.setattr(Renderer, "assemble", fake_assemble)
    renderer = Renderer()
    with raises(ValueError):
        assert renderer.output('flail').message == "Invalid output destination 'flail'"

#     def output(self, destination, filename=None):
#         """Actually put the image somewhere"""
#
#         self.assemble()
#
#         if destination == 'screen':
#             self.image.show()
#         elif destination == 'file':
#             if not filename:
#                 filename = ''.join([random.SystemRandom()
#                                    .choice(string.ascii_lowercase)
#                                    for n in range(8)])
#             self.image.save('output/' + filename + ".png", "PNG")
#         elif destination == 'variable':
#             return self.image
#         elif destination == 'dryrun':
#             # This doesn't actually do anything, but is handy for testing there
#             # are no material errors.
#             return
#         else:
#             raise ValueError("Invalid output destination '{}'"
#                              .format(destination))
