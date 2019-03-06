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

        with open(file) as json_file,\
                open('schemas/' + schema + '.json') as schema_file:

            file_json = json.load(json_file)
            schema_json = json.load(schema_file)

            validate(file_json, schema_json)
