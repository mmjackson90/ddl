"""
Tests example files to ensure we're shipping valid ones.
"""

from ddl.validator import Validator


def test_example_iso_pack():
    """ assetpacks/example_isometric/pack.json """
    Validator.validateFile('assetpacks/example_isometric/pack.json',
                           'pack')


def test_example_iso_images():
    """ assetpacks/example_isometric/images.json """
    Validator.validateFile('assetpacks/example_isometric/images.json',
                           'images')


def test_example_iso_components():
    """ assetpacks/example_isometric/components.json """
    Validator.validateFile('assetpacks/example_isometric/components.json',
                           'components')


def test_example_lowres_iso_pack():
    """ assetpacks/low_res_isometric/pack.json """
    Validator.validateFile('assetpacks/low_res_isometric/pack.json',
                           'pack')


def test_example_lowres_iso_images():
    """ assetpacks/low_res_isometric/images.json """
    Validator.validateFile('assetpacks/low_res_isometric/images.json',
                           'images')


def test_example_lowres_iso_components():
    """ assetpacks/low_res_isometric/components.json """
    Validator.validateFile('assetpacks/low_res_isometric/components.json',
                           'components')


def test_example_props_pack():
    """ assetpacks/example_props/pack.json """
    Validator.validateFile('assetpacks/example_props/pack.json',
                           'pack')


def test_example_props_images():
    """ assetpacks/example_props/images.json """
    Validator.validateFile('assetpacks/example_props/images.json',
                           'images')


def test_example_props_components():
    """ assetpacks/example_props/components.json """
    Validator.validateFile('assetpacks/example_props/components.json',
                           'components')
