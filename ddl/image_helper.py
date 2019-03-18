"""Tooling for interactively going through a directory of images and creating
the json representation of an AssetPack"""

import os
from glob import glob
from PIL import Image, ImageTk
import tkinter as tk
from ddl.cli_utils import *
from json import dumps
from PyInquirer import style_from_dict, Token, prompt, Separator


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


def show_directory(path):
    """Uses tkinter to iterate through a directory of images. Enter to move on."""

    root = tk.Tk()
    dirlist = glob(path+'/*.png')
    old_canvas = None
    print("LETS DO EET")
    all_image_data = []
    used_ids = []
    for filename in dirlist:
        image1 = Image.open(filename)
        image = Image.new("RGBA", image1.size, "WHITE")
        image.paste(image1, (0, 0), image1)
        tkpi = ImageTk.PhotoImage(image.convert('RGB'))

        grid_width = 294
        grid_height = 170
        next_action = ''
        offset_x = 0
        offset_y = 0
        while next_action != 'Next':
            choices = [{
                'type': 'list',
                'message': 'What would you like to do?',
                'name': 'next_action',
                'choices': [
                    'Next',
                    'Edit offset X',
                    'Edit offset Y'
                ]
            }]

            canvas = tk.Canvas(width=grid_width*3, height=grid_height*3, bg='white')

            canvas.create_image(grid_width*1.5-offset_x, grid_height-offset_y, image=tkpi, anchor=tk.NW)
            # AAAAAAA MUTATION
            add_iso_grid(canvas, grid_width, grid_height, grid_width*1.5, grid_height)

            canvas.pack()
            canvas.image = tkpi

            root.title(filename)
            if old_canvas is not None:
                old_canvas.destroy()
            old_canvas = canvas
            root.update_idletasks()
            root.update()
            next_action = prompt(choices, style=STYLE)['next_action']
            print("")
            if next_action == 'Edit offset Y':
                coordinates_questions = [{
                        'type': 'input',
                        'message': f"Current y offset: {offset_y}",
                        'name': 'y',
                        'validate': check_integer
                    }
                ]
                offset_y = int(prompt(coordinates_questions, style=STYLE)['y'])
            elif next_action == 'Edit offset X':
                coordinates_questions = [{
                        'type': 'input',
                        'message': f"Current x offset: {offset_x}",
                        'name': 'x',
                        'validate': check_integer
                    }
                ]
                offset_x = int(prompt(coordinates_questions, style=STYLE)['x'])
            print("")

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
        new_name = results['id']
        print(new_id in used_ids)
        image_data = {
            "name": new_name,
            "id": new_id,
            "image": filename,
            "top_left": {
                    "x": offset_x,
                    "y": offset_y
                }
            }
        used_ids = used_ids + [new_id]

        all_image_data = all_image_data+[image_data]
    print(dumps({"images": all_image_data}, indent=4))

if __name__ == '__main__':
    show_directory('assetpacks/example_isometric/art')
