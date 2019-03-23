"""Functions for the ddl_cli to use to explore an assetpack"""

from PyInquirer import prompt
from ddl.projection import IsometricProjection
from ddl.renderer import Renderer
from ddl.asset import ImageAsset
from ddl.cli_utils import *
import json


def show_pack_info(path):
    """Prints pack info to screen"""
    with open(path + '/pack.json') as pack_file:
        pack = json.load(pack_file)
        print(f"Name: {pack['name']}")
        print(f"Author: {pack['author']}")
        print(f"Projection: {pack['projection']}")
    print_tags(pack["tags"])


def show_projection_info(assetpack):
    """prints projection info to screen"""
    if isinstance(assetpack.projection, IsometricProjection):
        print("Type: Isometric")
    else:
        print("Type: Top Down")
    print(f"Grid height: {assetpack.projection.height} pixels.")
    print(f"Grid width: {assetpack.projection.width} pixels.")


def explore_assets(assetpack):
    """Lets the user interactively choose which components to look at next"""
    back = False
    while not back:
        explore = [{
            'type': 'list',
            'message': 'Which asset would you like to look at?',
            'name': 'choices',
            'choices': get_asset_choices(assetpack)
        }]
        choice = prompt(explore, style=STYLE)
        print("")
        option_chosen = choice['choices']
        if option_chosen == 'Back':
            back = True
        else:
            explore_asset(option_chosen, assetpack)
        print("")


def print_image_info(image):
    """Prints the info of an image asset"""
    print(f"Image name: {image.name}")
    print(f"Image ID: {image.asset_id}")
    print(f"Grid Top Left Corner pixel (x): {image.top_left['x']}")
    print(f"Grid Top Left Corner pixel (y): {image.top_left['y']}")


def print_component_info(component):
    """
    Prints the info of an component asset. May offer options to recursively
    explore in the future, but for now let's not.
    """
    print(f"Component name: {component.name}")
    print(f"Component ID: {component.asset_id}")
    print_tags(component.tags)
    print(f"Number of parts: {len(component.parts)}")


def show_component(assetpack, component):
    """Shows a component in it's own little window"""
    image_location_list = component.get_image_location_list(0, 0)
    renderer = Renderer(image_pixel_list=assetpack.projection
                        .get_image_pixel_list(0, 0, image_location_list))
    renderer.output('screen')


def get_asset(assetpack, initial_option):
    """Gets an asset from a choice made in a menu"""
    asset_type, asset_key = initial_option.split(': ')
    if asset_type == 'Image':
        asset = assetpack.images[asset_key]
    else:
        asset = assetpack.components[asset_key]
    return asset


def explore_asset(initial_option, assetpack):
    """Lets a user choose what they want to see about an asset"""
    asset = get_asset(assetpack, initial_option)
    explore = [{
        'type': 'list',
        'message': 'What would you like to do?',
        'name': 'choices',
        'choices': ['Show metadata',
                    'Show image',
                    'Show both']
    }]
    choice = prompt(explore, style=STYLE)
    print("")
    option_chosen = choice['choices']
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
