"""
Validator

Test files against the DDL schemas.
"""

import json

from jsonschema import validate


class Validator:

    @staticmethod
    def validateFile(file, schema):

        with open(file) as jsonFile,\
                open('schemas/' + schema + '.json') as schemaFile:

            fileJson = json.load(jsonFile)
            schemaJson = json.load(schemaFile)

            validate(fileJson, schemaJson)
