import click
from PyInquirer import style_from_dict, Token, prompt, Separator
import PyInquirer
from jsonschema.exceptions import ValidationError
from ddl.assetpack import AssetpackFactory
from ddl.validator import Validator
import ddl.asset_exploration
import ddl.image_helper
from ddl.asset import ComponentAsset
from ddl.cli_utils import *
import os


@click.group()
def main():
    """A CLI tool for validating and examining assetpacks, and in the future
    designing components, tweaking assetpacks and generally everything."""
    pass


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
        print(abs_path + '/pack.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

    try:
        Validator.validate_file(abs_path + '/images.json', 'images')
        images = True
        print("Images validated")
    except FileNotFoundError:
        print(error_header)
        print(abs_path + '/images.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

    try:
        filepath = abs_path + '/components.json'
        Validator.validate_file(filepath, 'components')
        components = True
        print("Components validated")
    except FileNotFoundError:
        print(error_header)
        print(abs_path + '/components.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

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
            'name': 'init',
            'choices': [
                'See pack information',
                'See projection information',
                'Explore Assets',
                'Quit'
            ]
        }]
        choice = prompt(init, style=STYLE)
        print("")
        option_chosen = choice['init']
        if option_chosen == 'Quit':
            exit_cli = True
        elif option_chosen == 'See pack information':
            ddl.asset_exploration.show_pack_info(path)
        elif option_chosen == 'See projection information':
            ddl.asset_exploration.show_projection_info(assetpack)
        elif option_chosen == 'Explore Assets':
            ddl.asset_exploration.explore_assets(assetpack)
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
    return ComponentAsset(data, assetpack.pack_id)


def get_component_build_choices(assetpack):
    """Get the choices of asset from an assetpack"""
    asset_choices = ['Done', Separator("Components")] +\
        list(map('Component: {}'.format,
                 assetpack.components.keys())) +\
        [Separator("Images")] +\
        list(map('Image: {}'.format,
                 assetpack.images.keys()))
    return asset_choices


@main.command()
@click.argument('path')
def create_new_component(path):
    """
    Lets a user interactively build a new component from an assetpack.

    path: The path of the asset pack directory.
    """
    path = os.path.abspath(path)
    assetpack = AssetpackFactory.load(path)
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
    info = prompt(component_info, style=STYLE)
    asset_choices = get_component_build_choices(assetpack)
    component = init_component(assetpack, info)
    done = False
    while not done:
        explore = [{
            'type': 'list',
            'message': 'Which asset would you like to look at?',
            'name': 'explore',
            'choices': asset_choices
        }]
        choice = prompt(explore, style=STYLE)
        print("")
        option_chosen = choice['explore']
        if option_chosen == 'Done':
            component.reset_sub_parts()
            print(component.get_json())
            ddl.asset_exploration.show_component(assetpack, component)
            done = True
        else:
            add_component(option_chosen, component, assetpack)
        print("")


@main.command()
@click.argument('path')
def create_new_images(path):
    """Iterates through all .png images in a directory and lets you set the information for them."""
    ddl.image_helper.show_directory(path)
