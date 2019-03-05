"""
Tests Assetpacks
"""

from ddl import AssetpackFactory, Assetpack

def test_assetpackfactory_creates_assetpack():
    assetpack = AssetpackFactory.load('example_isometric')
    assert type(assetpack) is Assetpack
