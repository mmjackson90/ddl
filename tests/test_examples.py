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
