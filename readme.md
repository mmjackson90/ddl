**Dungeon Definition Language

DDL is a suite of tools and definitions designed to make designing and illustrating full on D&D encounter maps much simpler. It consists of four rough parts:

1: The dungeon definition: This is only the bits the GM cares about. Important rooms etc. It can be used to create the spatial definition.

2: The spatial definition: This is computed from the above and describes the exact layout of the dungeon. It can be used to create the asset definition, given suitable assets.

3: The asset definition: This is made up of multiple assets, which may be made of assets, which are themselves images. This organises the spatial definition into a series of layers and images that can be pulled out into actual pretty pictures.

*Implementation
The tooling will be written (initially) in python. The definitions themselves will be json (see json-schema). Image handling done using pillow.
