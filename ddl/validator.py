"""
Validator

Test files against the DDL.
"""

import json

from jsonschema import validate


class Validator:
    """
    Validator

    Methods for ensuring files meet DDL requirements.
    """

    @staticmethod
    def validate_file(file, schema):
        """
        Load a file and then validate it against the given schema.
        """

        with open(file) as json_file:

            json_object = json.load(json_file)

            Validator.validate_json(json_object, schema)

    @staticmethod
    def validate_json(json_object, schema):
        """
        Validate the given JSON object against a schema.
        """

        with open('schemas/' + schema + '.json') as schema_file:

            schema_json = json.load(schema_file)

            validate(json_object, schema_json)
