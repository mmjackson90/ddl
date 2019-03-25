from pathlib import Path
import json
import logging


class DonjonParser:
    def __init__(self):
        self.parts = None

    def load_parts(self, filepath):
        logger = logging.getLogger('ddl')
        with open(filepath) as textFile:
            lines = [line.split('\t') for line in textFile]
            parts = []
            for y_coord in range(len(lines)):
                line = lines[y_coord]
                for x_coord in range(len(line)):
                    square = line[x_coord]
                    logger.debug('Tile at {},{} is: {}'.format(x_coord, y_coord, square))

                    if square not in ['', '\n']:
                        parts = parts + [{"x": x_coord,
                                          "y": y_coord,
                                          "layer": "floor",
                                          "constraints": ["floor"]}]
        self.parts = parts

    def save_parts(self, filepath, name, id):
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
