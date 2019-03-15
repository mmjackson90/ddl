#!/usr/bin/env python3

"""
A script to run an CLI in a variety of modes, some of which are
interactive
"""


import click
from PyInquirer import style_from_dict, Token, prompt
from jsonschema.exceptions import ValidationError

from ddl import AssetpackFactory
from ddl.validator import Validator
import ddl.asset_exploration


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
def main():
    """A CLI tool for validating and examining assetpacks, and in the future
    designing components, tweaking assetpacks and generally everything."""
    pass


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


if __name__ == "__main__":
    main()
