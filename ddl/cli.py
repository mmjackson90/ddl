"""Contains most of the functions for the CLI. Put here for testing purposes."""

import click
from PyInquirer import prompt
import PyInquirer
import jsonschema
from jsonschema.exceptions import ValidationError
from ddl.assetpack import AssetpackFactory
from ddl.validator import Validator
from ddl.renderer import Renderer
import ddl.asset_exploration
from ddl.asset_exploration import explore_assets, show_pack_info, show_projection_info
import ddl.image_helper
from ddl.asset import ComponentAsset
from ddl.cli_utils import *
import os
import logging
from ddl.blueprint import BlueprintFactory
import tkinter as tk
from PIL import Image, ImageTk
import random
from ddl.donjon_parser import DonjonParser


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def main(context, verbose):
    """A CLI tool for validating and examining assetpacks, and in the future
    designing components, tweaking assetpacks and generally everything."""

    context.ensure_object(dict)

    levels = {
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG
    }

    logger = logging.getLogger('ddl')
    logger.setLevel(levels.get(verbose, logging.INFO))
    logger.addHandler(logging.StreamHandler())

    logger.info('DDL CLI')

    context.obj['LOGGER'] = logger


@main.command()
@click.argument('path')
def validate_assetpack(path):
    """Validates an assetpack and errors if anything is wrong.

    path: The path of the asset pack directory.
    """
    pack = False
    images = False
    components = False
    error_header = '\n\n########ERROR########'

    abs_path = os.path.abspath(path)
    try:
        Validator.validate_file(abs_path + '/pack.json', 'pack')
        pack = True
        print("Pack validated")
    except FileNotFoundError:
        print(error_header)
        print(path + '/pack.json was not found.')
    except jsonschema.exceptions.ValidationError as val:
        print(error_header)
        print(val.message.split('/n')[0])
    except Exception:
        raise

    try:
        Validator.validate_file(abs_path + '/images.json', 'images')
        images = True
        print("Images validated")
    except FileNotFoundError:
        print(error_header)
        print(path + '/images.json was not found.')
    except jsonschema.exceptions.ValidationError as val:
        print(error_header)
        print(val.message.split('/n')[0])
    except Exception:
        raise

    try:
        filepath = abs_path + '/components.json'
        Validator.validate_file(filepath, 'components')
        components = True
        print("Components validated")
    except FileNotFoundError:
        print(error_header)
        print(path + '/components.json was not found.')
    except jsonschema.exceptions.ValidationError as val:
        print(error_header)
        print(val.message.split('/n')[0])
    except Exception:
        raise

    if pack and images and components:
        print("Validation passed. "+path+" is a good assetpack.")


@main.command()
@click.argument('path')
def explore_assetpack(path):
    """
    Lets a user interactively show things in an assetpack.

    path: The path of the asset pack directory.
    """
    path = os.path.abspath(path)
    assetpack = AssetpackFactory.load(path)
    exit_cli = False
    while not exit_cli:
        init = [{
            'type': 'list',
            'message': 'What would you like to do?',
            'name': 'choices',
            'choices': [
                'See pack information',
                'See projection information',
                'Explore Assets',
                'Quit'
            ]
        }]
        choice = prompt(init, style=STYLE)
        print("")
        option_chosen = choice['choices']
        if option_chosen == 'Quit':
            exit_cli = True
        elif option_chosen == 'See pack information':
            show_pack_info(path)
        elif option_chosen == 'See projection information':
            show_projection_info(assetpack)
        elif option_chosen == 'Explore Assets':
            explore_assets(assetpack)
        print("")


def validate_component_id(new_id, assetpack):
    """Validates a component ID against the IDS in an assetpack"""
    full_id = assetpack.pack_id + '.' + new_id
    if len(new_id) < 3:
        message = 'Try an ID with more than 2 characters.'
        raise PyInquirer.ValidationError(message=message)
    if full_id in assetpack.components.keys():
        message = 'This component name already exists in the assetpack.'
        raise PyInquirer.ValidationError(message=message)
    return True


def add_component(initial_option, component, assetpack):
    """Lets a user choose what they want to see about an asset"""
    asset_type, asset_key = initial_option.split(': ')
    coordinates_questions = [{
            'type': 'input',
            'message': 'Where is this in the x dimension?',
            'name': 'x',
            'validate': check_number
        },
        {
            'type': 'input',
            'message': 'Where is this in the y dimension?',
            'name': 'y',
            'validate': check_number
        }
    ]
    coordinates = prompt(coordinates_questions, style=STYLE)
    component_x = float(coordinates['x'])
    component_y = float(coordinates['y'])
    if asset_type == 'Image':
        asset = assetpack.images[asset_key]
        component.add_image(asset,
                            component_x,
                            component_y)
    else:
        asset = assetpack.components[asset_key]
        component.add_component(asset,
                                component_x,
                                component_y)


def init_component(assetpack, info):
    """Initialise a blank component"""
    component_name = info['component_name']
    component_id = info['component_id']
    component_tags = list(map(str.strip, info['component_tags'].split(',')))
    component_parts = []
    data = {
        "name": component_name,
        "id": component_id,
        "parts": component_parts,
        "tags": component_tags
    }
    return ComponentAsset(data, assetpack)


def choose_asset(component, asset_choices, assetpack):
    """The options for the inside of the Add component loop"""
    explore = [{
        'type': 'list',
        'message': 'Which asset would you like to add?',
        'name': 'explore',
        'choices': asset_choices
    }]
    choice = prompt(explore, style=STYLE)
    print("")
    option_chosen = choice['explore']
    if not option_chosen == 'Back':
        add_component(option_chosen, component, assetpack)


def reset_component_window(component, assetpack, root, old_canvas):
    """clears and redraws the component window"""
    component.instantiate_sub_parts()
    image_location_list = component.get_image_location_list(0, 0)
    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    orig_image = renderer.output('variable')
    image = get_rgb_image(orig_image)
    canvas = tk.Canvas(width=orig_image.width, height=orig_image.height, bg='white')
    canvas.create_image(0, 0, image=image, anchor=tk.NW)
    canvas.pack()
    canvas.image = image

    if old_canvas is not None:
        old_canvas.destroy()

    old_canvas = canvas
    root.update_idletasks()
    root.update()
    return old_canvas


def get_initial_component_info(assetpack):
    """Gets new component info from user"""
    component_info = [{
            'type': 'input',
            'message': 'What would you like to call this component?',
            'name': 'component_name'
        },
        {
            'type': 'input',
            'message': 'What ID would you like to give this component?',
            'name': 'component_id',
            'validate': lambda new_id: validate_component_id(new_id, assetpack)
        },
        {
            'type': 'input',
            'message': 'What tags should the component have?',
            'name': 'component_tags'
        }
    ]
    return prompt(component_info, style=STYLE)


@main.command()
@click.argument('path')
def create_new_component(path):
    """
    Lets a user interactively build a new component from an assetpack.

    path: The path of the asset pack directory.
    """
    path = os.path.abspath(path)
    assetpack = AssetpackFactory.load(path)
    info = get_initial_component_info(assetpack)
    root = tk.Tk()
    root.title(info['component_id'])
    asset_choices = get_asset_choices(assetpack)
    component = init_component(assetpack, info)
    old_canvas = None
    choice = ''
    while not choice == 'Done':
        choices = [{
            'type': 'list',
            'message': 'What would you like to do?',
            'name': 'choice',
            'choices': ['Add an asset', 'Done', 'Undo']
        }]
        choice = prompt(choices, style=STYLE)['choice']
        if choice == 'Add an asset':
            choose_asset(component, asset_choices, assetpack)
        elif choice == 'Undo':
            component.remove_last_part()
        old_canvas = reset_component_window(component, assetpack, root, old_canvas)
        print("")
    component.reset_sub_parts()
    print(component.get_json())


@main.command()
@click.argument('path')
@click.option('--gridtype', type=click.Choice(['isometric', 'topdown']), prompt=True)
@click.option('--width', prompt=True)
@click.option('--height', prompt=True)
def create_new_images(path, gridtype, width, height):
    """Iterates through all .png images in a directory and lets you set the information for them."""
    check_integer(width)
    check_integer(height)

    ddl.image_helper.show_directory(path, gridtype, int(height), int(width))


@main.command()
@click.argument('blueprint_file', type=click.Path(exists=True))
@click.argument('assetpack_file', type=click.Path(exists=True))
@click.pass_context
def build(context, blueprint_file, assetpack_file):
    """ Build a blueprint file, and output an image. """

    logger = context.obj['LOGGER']

    logger.info('Building Blueprint')

    blueprint = BlueprintFactory.load(click.format_filename(blueprint_file))

    logger.debug('Loaded blueprint from {}'.format(click.format_filename(blueprint_file)))

    assetpack = AssetpackFactory.load(click.format_filename(assetpack_file))

    logger.debug('Loaded single asset pack from {}'.format(click.format_filename(blueprint_file)))

    data = {
        "name": '',
        "id": 'build',
        "parts": [],
        "tags": []
    }
    component = ComponentAsset(data, assetpack)
    logger.info('Finding appropriate tiles and adding to component')
    for (tile_x, tile_y), tile in blueprint.get_constraints_in_layer('floor').items():
        logger.debug('Tile at ({}, {}) has constraints {}'.format(tile_x, tile_y, ', '.join(tile)))
        valid_components = assetpack.taglist.get_components_that_match_tags(tile)

        if valid_components:
            logger.debug('Matching components are: {}'.format(', '.join(valid_components)))
            choice = random.sample(valid_components, 1)[0]
            component.add_component(assetpack.components[choice], tile_x, tile_y)
        else:
            raise Exception('No matching components for given constraints.')

    logger.info('Getting image/pixel list')
    image_location_list = component.get_image_location_list(0, 0)
    image_pixel_list = assetpack.projection.\
        get_image_pixel_list(0, 0, image_location_list)
    logger.info('Preparing render')
    renderer = Renderer(image_pixel_list=image_pixel_list)
    logger.info('Rendering')
    renderer.output('screen')
    logger.info('Done')


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file')
@click.argument('blueprint_name')
@click.argument('blueprint_id')
@click.pass_context
def convert_donjon(context, input_file, output_file, blueprint_name, blueprint_id):
    logger = context.obj['LOGGER']
    parser = DonjonParser()
    logger.info('Converting {} to blueprint'.format(input_file))
    parser.load_parts(input_file)
    parser.save_parts(output_file, blueprint_name, blueprint_id)
    logger.info('Output finished blueprint to {}'.format(output_file))
