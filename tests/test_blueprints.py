"""
Tests example files to ensure we're shipping valid ones.
"""

from ddl.blueprint import BlueprintFactory


def test_load_from_file():
    """Tests a blueprint loads and that's about it."""
    blueprint = BlueprintFactory.load('blueprints/examples/dungeon-3x3.json')
    assert len(blueprint.layers['floor']) == 9
