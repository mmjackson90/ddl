"""Contains a parser class for donjon files"""

from pathlib import Path
import json
import logging


class DonjonParser:
    """A class for parsing Donjob TSV files and spitting out blueprints.
    Currently only creates floorplans, but later should allow for further customisation.
    """
    def __init__(self):
        self.parts = None

    def load_parts(self, filepath):
        """Loads a Donjon TSV into the parser and turns it into a list of floors,
        randomly choosing a valid tile if more than one is available"""
        logger = logging.getLogger('ddl')
        with open(filepath) as tsv_file:
            lines = [line.split('\t') for line in tsv_file]
            parts = []
            for y_coord, line in enumerate(lines):
                for x_coord, square in enumerate(line):
                    logger.debug('Tile at {},{} is: {}'.format(x_coord, y_coord, square))

                    if square not in ['', '\n']:
                        parts = parts + [{"x": x_coord,
                                          "y": y_coord,
                                          "layer": "floor",
                                          "constraints": ["floor"]}]
        self.parts = parts

    def save_parts(self, filepath, name, id):
        """Save out a neatly parsed Donjon Blueprint file."""
        if self.parts is None:
            raise ValueError("No file loaded")

        component_data = {
            "name": name,
            "id": id,
            "parts": self.parts
        }

        filename = Path(filepath)
        filename.touch(exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(component_data, file)
