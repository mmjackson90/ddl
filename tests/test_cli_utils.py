from ddl.cli_utils import *
import ddl.cli_utils
import PyInquirer
from pytest import raises
from PIL import Image, ImageTk
import tkinter as tk


def test_tag_printing(capsys):
    """Tests tags print right"""
    tags = ['a', 'b', 'c']
    print_tags(tags)
    captured = capsys.readouterr()
    assert captured.out == 'Tags:\n    a\n    b\n    c\n'


def test_check_number():
    """Tests number validation"""
    assert check_number('5')
    assert check_number('5.5')
    with raises(PyInquirer.ValidationError):
        assert check_number('fish') is False


def test_check_integer():
    """Tests integer validation"""
    assert check_integer('5')
    with raises(PyInquirer.ValidationError):
        assert check_integer('5.5') is False
    with raises(PyInquirer.ValidationError):
        assert check_integer('fish') is False


def test_get_rgb_image():
    """Tests an image converts to tkinter image object OK."""
    root = tk.Tk()
    input_image = Image.open('assetpacks/example_isometric/art/1_wall_exact.png')
    assert isinstance(get_rgb_image(input_image), ImageTk.PhotoImage)


def test_get_asset_choices(monkeypatch):
    def fake_separator(string):
        return string
    """Tests that asset choices are correctly parsed from assetpack"""
    class FakePack:
        def __init__(self):
            self.images = {'test.image1': 1,
                           'test.image2': 2}
            self.components = {'test.component1': 1,
                               'test.component2': 2}
    assetpack = FakePack()
    monkeypatch.setattr(ddl.cli_utils, "Separator", fake_separator)
    assert get_asset_choices(assetpack) == ['Back', 'Components',
                                            'Component: test.component1',
                                            'Component: test.component2',
                                            'Images',
                                            'Image: test.image1',
                                            'Image: test.image2']


def test_validate_image_id():
    """tests image ID's validate correctly"""
    used_ids = ['test']
    assert validate_image_id('thing', used_ids)
    with raises(PyInquirer.ValidationError):
        assert validate_image_id('a', used_ids).message == "Try an ID with more than 2 characters."
    with raises(PyInquirer.ValidationError):
        assert validate_image_id('test test ', used_ids).message == "Please don't use whitespace for ID's"
    with raises(PyInquirer.ValidationError):
        assert validate_image_id('test', used_ids).message == "This image name already exists."
