#!/usr/bin/env python3

import click
from PyInquirer import style_from_dict, Token, prompt, Separator
from jsonschema.exceptions import ValidationError

from ddl import AssetpackFactory
from ddl.validator import Validator
from ddl.projection import IsometricProjection

import json


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
    """The main function for handling the rest of the jazz"""
    pass


@main.command()
@click.argument('name')
def validate_assetpack(name):
    """Validates an assetpack and printes errors if anything is off"""
    pack = False
    images = False
    component = False
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
    """Lets a user interactively show things in an assetpack"""
    assetpack = AssetpackFactory.load(name)
    quit = False
    while not quit:
        init = [{
            'type': 'list',
            'message': 'What would you like to do?',
            'name': 'init',
            'choices': [
                'See pack information',
                'See projection information',
                'Quit'
            ]
        }]
        choice = prompt(init, style=STYLE)
        print("")
        option_chosen = choice['init']
        if option_chosen == 'Quit':
            quit = True
        elif option_chosen == 'See pack information':
            show_pack_info(name)
        elif option_chosen == 'See projection information':
            show_projection_info(assetpack)
        print("")


def show_pack_info(name):
    with open('assetpacks/' + name + '/pack.json') as pack_file:
        pack = json.load(pack_file)
        print(f"Name: {pack['name']}")
        print(f"Author: {pack['author']}")
        print(f"Projection: {pack['projection']}")
        print("Tags:")
        for tag in pack["tags"]:
            print(f"    {tag}")


def show_projection_info(assetpack):
    if isinstance(assetpack.projection, IsometricProjection):
        print("Type: Isometric")
    else:
        print("Type: Top Down")
    print(f"Grid height: {assetpack.projection.height} pixels.")
    print(f"Grid width: {assetpack.projection.width} pixels.")


if __name__ == "__main__":
    main()
