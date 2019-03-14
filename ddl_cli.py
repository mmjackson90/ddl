#!/usr/bin/env python3

import click
from PyInquirer import style_from_dict, Token, prompt, Separator
from jsonschema.exceptions import ValidationError

from ddl import AssetpackFactory
from ddl.validator import Validator
from ddl.projection import IsometricProjection
from ddl.asset import ImageAsset, ComponentAsset
from ddl.renderer import Renderer

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
    """
    Lets a user interactively show things in an assetpack.

    name: The name of an assetpack in the current assetpack structure.
    """
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
                'Explore Assets',
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
        elif option_chosen == 'Explore Assets':
            explore_assets(assetpack)
        print("")


def print_tags(tags):
    print("Tags:")
    for tag in tags:
        print(f"    {tag}")


def show_pack_info(name):
    with open('assetpacks/' + name + '/pack.json') as pack_file:
        pack = json.load(pack_file)
        print(f"Name: {pack['name']}")
        print(f"Author: {pack['author']}")
        print(f"Projection: {pack['projection']}")
    print_tags(pack["tags"])


def show_projection_info(assetpack):
    if isinstance(assetpack.projection, IsometricProjection):
        print("Type: Isometric")
    else:
        print("Type: Top Down")
    print(f"Grid height: {assetpack.projection.height} pixels.")
    print(f"Grid width: {assetpack.projection.width} pixels.")


def explore_assets(assetpack):
    asset_choices = ['Back', Separator("Components")] +\
                    list(map('Component: {}'.format,
                             assetpack.components.keys())) +\
                    [Separator("Images")] +\
                    list(map('Image: {}'.format,
                             assetpack.images.keys()))
    back = False
    while not back:
        explore = [{
            'type': 'list',
            'message': 'Which asset would you like to look at?',
            'name': 'explore',
            'choices': asset_choices
        }]
        choice = prompt(explore, style=STYLE)
        print("")
        option_chosen = choice['explore']
        if option_chosen == 'Back':
            back = True
        else:
            explore_asset(option_chosen, assetpack)
        print("")


def print_image_info(image):
    print(f"Image name: {image.name}")
    print(f"Image ID: {image.asset_id}")
    print(f"Grid Top Left Corner pixel (x): {image.top_left['x']}")
    print(f"Grid Top Left Corner pixel (y): {image.top_left['y']}")


def print_component_info(component):
    print(f"Component name: {component.name}")
    print(f"Component ID: {component.asset_id}")
    print_tags(component.tags)
    print(f"Number of parts: {len(component.parts)}")


def show_component(assetpack, component):
    image_location_list = assetpack.get_image_location_list(0, 0, component)
    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('screen')


def explore_asset(initial_option, assetpack):
    asset_type, asset_key = initial_option.split(': ')
    if asset_type == 'Image':
        asset = assetpack.images[asset_key]
    else:
        asset = assetpack.components[asset_key]
    explore = [{
        'type': 'list',
        'message': 'What would you like to do?',
        'name': 'asset',
        'choices': ['Show metadata',
                    'Show image',
                    'Show both']
    }]
    choice = prompt(explore, style=STYLE)
    print("")
    option_chosen = choice['asset']
    if option_chosen == 'Show metadata':
        if (isinstance(asset, ImageAsset)):
            print_image_info(asset)
        else:
            print_component_info(asset)
    elif option_chosen == 'Show image':
        if (isinstance(asset, ImageAsset)):
            asset.show()
        else:
            show_component(assetpack, asset)
    else:
        if (isinstance(asset, ImageAsset)):
            print_image_info(asset)
            asset.show()
        else:
            print_component_info(asset)
            show_component(assetpack, asset)

    print("")

if __name__ == "__main__":
    main()
