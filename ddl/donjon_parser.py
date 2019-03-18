class DonjonParser:
    def load_parts(filepath):
        with open("/Users/Casual/Downloads/dungeon_01.txt") as textFile:
            lines = [line.split('\t') for line in textFile]
            parts = []
            for y_coord in range(len(lines)):
                line = lines[y_coord]
                for x_coord in range(len(line)):
                    parts = parts + [{"x": x_coord,
                                      "y": y_coord,
                                      "constraints": ["floor"]}]
            return parts
