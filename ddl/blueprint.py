"""
Blueprints
"""

import json

from ddl.validator import Validator


class BlueprintFactory:
    """Create a Blueprint from a JSON file"""

    @staticmethod
    def load(name):
        """Loads AssetPacks from their component and Image packs,
         given an appropriate name"""
        with open(
                'blueprints/' + name + '.json'
                ) as blueprint_file:
            blueprint = json.load(blueprint_file)

            # Test this JSON is valid
            Validator.validate_json(blueprint, 'blueprint')

            return Blueprint(blueprint)


class Blueprint:

    def __init__(self, blueprint):
        pass
