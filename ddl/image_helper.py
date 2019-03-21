"""Tooling for interactively going through a directory of images and creating
the json representation of an AssetPack"""

from glob import glob
from PIL import Image
import tkinter as tk
from ddl.cli_utils import *
from json import dumps
from PyInquirer import prompt


def add_iso_grid(canvas, grid_width, grid_height, x_offset, y_offset):
    """Will add an ISO grid to a canvas.
    ###THIS FUNCTION IS HIGHLY MUTAGENIC - HANDLE WITH CARE###
    """
    left = x_offset-grid_width/2
    right = grid_width/2 + x_offset
    x_mid = x_offset
    top = y_offset
    bottom = grid_height + y_offset
    y_mid = y_offset + grid_height/2

    canvas.create_line(x_mid, top, left, y_mid, width=2, fill="red")
    canvas.create_line(x_mid, top, right, y_mid, width=2, fill="red")
    canvas.create_line(x_mid, bottom, left, y_mid, width=2, fill="red")
    canvas.create_line(x_mid, bottom, right, y_mid, width=2, fill="red")


def add_topdown_grid(canvas, grid_width, grid_height, x_offset, y_offset):
    """Will add an ISO grid to a canvas.
    ###THIS FUNCTION IS HIGHLY MUTAGENIC - HANDLE WITH CARE###
    """
    left = x_offset
    right = grid_width + x_offset
    bottom = grid_height + y_offset
    top = y_offset

    canvas.create_line(right, top, left, top, width=2, fill="red")
    canvas.create_line(right, bottom, left, bottom, width=2, fill="red")
    canvas.create_line(right, top, right, bottom, width=2, fill="red")
    canvas.create_line(left, top, left, bottom, width=2, fill="red")


def get_image_metadata(used_ids, filename, offset_x, offset_y):
    """Pushes all the image metadata (new id and image data as it will be in
    the .json) out"""
    id_questions = [{
            'type': 'input',
            'message': f"Please give this image an ID",
            'name': 'id',
            'validate': lambda new_id: validate_image_id(new_id, used_ids)
        },
        {
            'type': 'input',
            'message': f"and a nice descriptive name.",
            'name': 'name'
        }
    ]
    results = prompt(id_questions, style=STYLE)
    new_id = results['id']
    new_name = results['name']
    image_data = {
        "name": new_name,
        "id": new_id,
        "image": filename.split('/')[-1],
        "top_left": {
                "x": offset_x,
                "y": offset_y
            }
        }
    return (new_id, image_data)


def update_offset(offset, dimension):
    """Will prompt the user for a new offset and return it."""
    coordinates_questions = [{
            'type': 'input',
            'message': f"Current {dimension} offset: {offset}",
            'name': f"{dimension}",
            'validate': check_integer
        }
    ]
    return int(prompt(coordinates_questions, style=STYLE)[dimension])


def get_next_action():
    """Gets the next option the user wants from a simple list"""
    choices = [{
        'type': 'list',
        'message': 'What would you like to do?',
        'name': 'next_action',
        'choices': [
            'Next',
            'Skip',
            'Edit offset X',
            'Edit offset Y',
            'Quit now'
        ]
    }]
    return prompt(choices, style=STYLE)['next_action']


def positioning_loop(root, grid_type, grid_width, grid_height, image, old_canvas):
    next_action = ''
    offset_x = 0
    offset_y = 0
    while next_action not in ['Next', 'Quit now', 'Skip']:
        canvas = tk.Canvas(width=grid_width*3, height=grid_height*3, bg='white')

        # AAAAAAA MUTATION
        if grid_type == 'isometric':
            canvas.create_image(grid_width*1.5-offset_x, grid_height-offset_y, image=image, anchor=tk.NW)
            add_iso_grid(canvas, grid_width, grid_height, grid_width*1.5, grid_height)
        else:
            canvas.create_image(grid_width-offset_x, grid_height-offset_y, image=image, anchor=tk.NW)
            add_topdown_grid(canvas, grid_width, grid_height, grid_width, grid_height)

        canvas.pack()
        canvas.image = image

        if old_canvas is not None:
            old_canvas.destroy()
        old_canvas = canvas
        root.update_idletasks()
        root.update()
        next_action = get_next_action()
        print("")
        if next_action == 'Edit offset Y':
            offset_y = update_offset(offset_y, 'y')
        elif next_action == 'Edit offset X':
            offset_x = update_offset(offset_x, 'x')
        print("")
    return (offset_x, offset_y, next_action, old_canvas)


def show_directory(path, grid_type, grid_height, grid_width):
    """Uses tkinter to iterate through a directory of images. Enter to move on."""

    root = tk.Tk()
    dirlist = glob(path+'/*.png')
    old_canvas = None
    all_image_data = []
    used_ids = []
    for filename in dirlist:
        root.title(filename)
        image = get_rgb_image(Image.open(filename))
        offset_x, offset_y, next_action, old_canvas = positioning_loop(root,
                                                                       grid_type,
                                                                       grid_width,
                                                                       grid_height,
                                                                       image,
                                                                       old_canvas)
        if next_action == 'Quit now':
            break
        if not next_action == 'Skip':
            image_metadata = get_image_metadata(used_ids, filename, offset_x, offset_y)
            used_ids = used_ids + [image_metadata[1]]
            all_image_data = all_image_data+[image_metadata[1]]

    print(dumps({"images": all_image_data}, indent=4))
