import os
from PIL import Image, ImageTk
import tkinter as tk
from ddl.asset_exploration import print_tags

from PyInquirer import style_from_dict, Token, prompt, Separator

STYLE = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def add_iso_grid(canvas, grid_width, grid_height, x_offset, y_offset):
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
    dirlist = os.listdir(path)
    old_canvas = None
    print("LETS DO EET")
    for f in dirlist:
        print(f)

        image1 = Image.open(path+'/'+f)
        image = Image.new("RGBA", image1.size, "WHITE")
        image.paste(image1, (0, 0), image1)
        tkpi = ImageTk.PhotoImage(image.convert('RGB'))

        grid_width = 294
        grid_height = 170
        next_action = ''
        offset_x = 0
        offset_y = 0
        tags = []
        while next_action != 'Next':
            exit_cli = False
            choices = [{
                'type': 'list',
                'message': 'What would you like to do?',
                'name': 'next_action',
                'choices': [
                    'Next',
                    'Edit offset X',
                    'Edit offset Y',
                    'Edit tags'
                ]
            }]

            canvas = tk.Canvas(width=grid_width*3, height=grid_height*3, bg='white')

            # pack the canvas into a frame/form
            image_ref = canvas.create_image(grid_width*1.5-offset_x, grid_height-offset_y, image=tkpi, anchor=tk.NW)
            # AAAAAAA MUTATION
            add_iso_grid(canvas, grid_width, grid_height, grid_width*1.5, grid_height)

            canvas.pack()
            canvas.image = tkpi

            root.title(f)
            if old_canvas is not None:
                old_canvas.destroy()
            old_canvas = canvas
            root.update_idletasks()
            root.update()
            next_action = prompt(choices, style=STYLE)['next_action']
            print("")
            if next_action == 'Edit offset X':
                print(f"Current x offset: {offset_x}")
                offset_x = int(input())
            elif next_action == 'Edit offset Y':
                print(f"Current y offset: {offset_y}")
                offset_y = int(input())
            elif next_action == 'Edit tags':
                print_tags(tags)
                tags = list(map(str.strip, input().split(',')))
            print("")


if __name__ == '__main__':
    show_directory('assetpacks/example_isometric/art')
