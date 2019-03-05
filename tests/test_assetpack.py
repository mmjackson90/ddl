"""
Tests Assetpacks
"""

from ddl import AssetpackFactory, Assetpack


def test_factory_creates_assetpack():
    """ Ensure the AssetpackFactory returns an Assetpack. """
    assetpack = AssetpackFactory.load('example_isometric')
    if not isinstance(assetpack, Assetpack):
        raise AssertionError()
