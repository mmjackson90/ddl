"""tests the image_helper functions"""

from ddl.image_helper import *

import ddl.image_helper
from glob import glob
from PIL import Image
import tkinter as tk
from json import dumps
from PyInquirer import prompt

global PROMPT_CALLS
PROMPT_CALLS = 0


def test_add_iso_grid():
    """Tests the add_iso_grid properly mutates a canvas object"""
    class FakeCanvas:
        def __init__(self):
            self.results = []

        def create_line(self, p1_x, p1_y, p2_x, p2_y, width=0, fill='green'):
            self.results.append((p1_x, p1_y, p2_x, p2_y, width, fill))

    canvas = FakeCanvas()
    add_iso_grid(canvas, 10, 20, 2, 3)
    assert len(canvas.results) == 4
    assert canvas.results[0] == (2, 3, -3, 13, 2, 'red')
    assert canvas.results[1] == (2, 3, 7, 13, 2, 'red')
    assert canvas.results[2] == (2, 23, -3, 13, 2, 'red')
    assert canvas.results[3] == (2, 23, 7, 13, 2, 'red')


def test_add_topdown_grid():
    """Tests the add_topdown_grid properly mutates a canvas object"""
    class FakeCanvas:
        def __init__(self):
            self.results = []

        def create_line(self, p1_x, p1_y, p2_x, p2_y, width=0, fill='green'):
            self.results.append((p1_x, p1_y, p2_x, p2_y, width, fill))

    canvas = FakeCanvas()
    add_topdown_grid(canvas, 10, 20, 2, 3)
    assert len(canvas.results) == 4
    assert canvas.results[0] == (12, 3, 2, 3, 2, 'red')
    assert canvas.results[1] == (12, 23, 2, 23, 2, 'red')
    assert canvas.results[2] == (12, 3, 12, 23, 2, 'red')
    assert canvas.results[3] == (2, 3, 2, 23, 2, 'red')


def test_create_new_component(monkeypatch):
    """FUNCTIONALTests that components can be created neatly"""
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        global PROMPT_CALLS
        choices = [
            {'id': 'test', 'name': 'test name'}
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.image_helper, "prompt", fakeprompt)
    assert get_image_metadata([], 'test1/test2.png', 2, 3) == ('test', {
                                                                "name": 'test name',
                                                                "id": 'test',
                                                                "image": 'test2.png',
                                                                "top_left": {
                                                                            "x": 2,
                                                                            "y": 3
                                                                    }
                                                                })


def test_update_offset(monkeypatch):
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        global PROMPT_CALLS
        choices = [
            {'x': 2},
            {'y': 3}
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.image_helper, "prompt", fakeprompt)
    assert update_offset(0, 'x') == 2
    assert update_offset(0, 'y') == 3
