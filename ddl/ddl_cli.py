#!/usr/bin/env python3

import click
from validator import Validator
from jsonschema.exceptions import ValidationError


@click.group()
def main():
    """The main function for handling the rest of the jazz"""
    pass


@main.command()
@click.argument('name')
def validate_assetpack(name):
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


if __name__ == "__main__":
    main()
