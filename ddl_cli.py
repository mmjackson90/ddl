#!/usr/bin/env python3

"""
A script to run an CLI in a variety of modes, some of which are
interactive
"""


import click
import logging

from PyInquirer import style_from_dict, Token, prompt, Separator
import PyInquirer
from jsonschema.exceptions import ValidationError

from ddl.assetpack import AssetpackFactory
from ddl.validator import Validator
import ddl.asset_exploration
from ddl.asset import ComponentAsset
from ddl.blueprint import BlueprintFactory


STYLE = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


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
@click.argument('name')
def validate_assetpack(name):
    """Validates an assetpack and errors if anything is wrong.

    name: The name of an assetpack in the current assetpack structure.
    """
    pack = False
    images = False
    components = False
    error_header = '\n\n########ERROR########'

    try:
        Validator.validate_file('assetpacks/' + name + '/pack.json',
                                'pack')
        pack = True
        print("Pack validated")
    except FileNotFoundError:
        print(error_header)
        print('assetpacks/' + name + '/pack.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

    try:
        Validator.validate_file('assetpacks/' + name + '/images.json',
                                'images')
        images = True
        print("Images validated")
    except FileNotFoundError:
        print(error_header)
        print('assetpacks/' + name + '/images.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

    try:
        filepath = 'assetpacks/' + name + '/components.json'
        Validator.validate_file(filepath, 'components')
        components = True
        print("Components validated")
    except FileNotFoundError:
        print(error_header)
        print('assetpacks/' + name + '/components.json was not found.')
    except ValidationError as val:
        print(error_header)
        print(str(val))

    if pack and images and components:
        print("Validation passed. "+name+" is a good assetpack.")


@main.command()
@click.argument('name')
def explore_assetpack(name):
    """
    Lets a user interactively show things in an assetpack.

    name: The name of an assetpack in the current assetpack structure.
    """
    assetpack = AssetpackFactory.load(name)
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
            ddl.asset_exploration.show_pack_info(name)
        elif option_chosen == 'See projection information':
            ddl.asset_exploration.show_projection_info(assetpack)
        elif option_chosen == 'Explore Assets':
            ddl.asset_exploration.explore_assets(assetpack)
        print("")


def validate_component_id(new_id, assetpack):
    """Validates a component ID against the IDS in an assetpack"""
    full_id = assetpack.name + '.' + new_id
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


def check_number(string):
    """Checks a string can be parsed to a number"""
    try:
        float(string)
        return True
    except ValueError:
        message = 'Please input a number.'
        raise PyInquirer.ValidationError(message=message)


@main.command()
@click.argument('name')
def create_new_component(name):
    """
    Lets a user interactively build a new component from an assetpack.

    name: The name of an assetpack in the current assetpack structure.
    """
    assetpack = AssetpackFactory.load(name)
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
    component_name = info['component_name']
    component_id = info['component_id']
    component_tags = info['component_tags'].split(',')
    component_parts = []
    data = {
        "name": component_name,
        "id": component_id,
        "parts": component_parts,
        "tags": component_tags
    }
    component = ComponentAsset(data, assetpack.name)

    asset_choices = ['Done', Separator("Components")] +\
        list(map('Component: {}'.format,
                 assetpack.components.keys())) +\
        [Separator("Images")] +\
        list(map('Image: {}'.format,
                 assetpack.images.keys()))
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

    for (tile_x, tile_y), tile in blueprint.get_constraints_in_layer('floor').items():
        logger.debug('Tile at ({}, {}) has constraints {}'.format(tile_x, tile_y, ', '.join(tile)))
        valid_components = assetpack.taglist.get_components_that_match_tags(tile)

        if valid_components:
            logger.debug('Matching components are: {}'.format(', '.join(valid_components)))
        else:
            raise Exception('No matching components for given constraints.')


if __name__ == "__main__":
    main()
