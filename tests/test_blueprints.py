"""
Tests example files to ensure we're shipping valid ones.
"""

from ddl.blueprint import BlueprintFactory


def test_load_from_file():

    blueprint = BlueprintFactory.load('examples/dungeon-3x3')
