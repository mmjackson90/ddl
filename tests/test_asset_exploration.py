"""Tests the asset exploration functions of the CLI (which are interactive)
These are deliberately part-integration rather than unit, as the important thing for the
CLI is that the methods be called consistently."""

import ddl.asset_exploration
from ddl.assetpack import Assetpack
from ddl.asset import ImageAsset, ComponentAsset
from ddl.projection import IsometricProjection, TopDownProjection


def get_test_assetpack():
    return Assetpack('test', 'assetpacks/low_res_isometric',
                     {"images": [
                              {
                                  "name": "1x1 Floor low_res",
                                  "id": "c",
                                  "image": "1x1_floor_low_res.png",
                                  "top_left": {
                                      "x": 73,
                                      "y": 0
                                  }
                              }
                            ]},
                     {"components": [
                              {
                                  "name": "test Floor low_res",
                                  "id": "a",
                                  "parts": [
                                      {
                                          "type": "image",
                                          "image_id": "floor-1x1-low-res",
                                          "x": 0,
                                          "y": 0
                                      }
                                  ],
                                  "tags": [
                                      "example"
                                  ]
                              },
                              {
                                  "name": "test Floor low_res",
                                  "id": "b",
                                  "parts": [
                                      {
                                          "type": "image",
                                          "image_id": "floor-1x1-low-res",
                                          "x": 0,
                                          "y": 0
                                      }
                                  ],
                                  "tags": [
                                      "example"
                                  ]
                              }
                          ],
                      "grid": {"type": "isometric",
                               "width": 10,
                               "height": 20}})


def test_tag_printing(capsys):
    tags = ['a', 'b', 'c']
    ddl.asset_exploration.print_tags(tags)
    captured = capsys.readouterr()
    assert captured.out == 'Tags:\n    a\n    b\n    c\n'


def test_show_pack_info(capsys, monkeypatch):
    # Mostly this is to test that capsys and monkeypatch work the way I expect.
    def faketags(tags):
        pass
    monkeypatch.setattr(ddl.asset_exploration, "print_tags", faketags)
    ddl.asset_exploration.show_pack_info('assetpacks/example_isometric')
    captured = capsys.readouterr()
    assert captured.out == """Name: Example Isometric Asset Pack
Author: The DDL Team
Projection: isometric
"""


def test_show_projection_isometric(capsys):
    assetpack = get_test_assetpack()
    ddl.asset_exploration.show_projection_info(assetpack)
    captured = capsys.readouterr()
    assert captured.out == """Type: Isometric
Grid height: 20 pixels.
Grid width: 10 pixels.
"""


def test_get_asset_choices(capsys, monkeypatch):
    assetpack = get_test_assetpack()
    choices = ddl.asset_exploration.get_asset_choices(assetpack)
    assert choices[0] == 'Back'
    assert choices[2] == 'Component: test.a'
    assert choices[3] == 'Component: test.b'
    assert choices[5] == 'Image: test.c'


def test_print_image_info(capsys):
    image = ImageAsset({"name": 'image',
                        "id": "image_id",
                        "image": "1x1_floor_low_res.png",
                        "top_left": {"x": 2,
                                     "y": 3}
                        },
                       'test',
                       'assetpacks/low_res_isometric')
    ddl.asset_exploration.print_image_info(image)
    captured = capsys.readouterr()
    assert captured.out == """Image name: image
Image ID: image_id
Grid Top Left Corner pixel (x): 2
Grid Top Left Corner pixel (y): 3
"""


def test_print_component_info(capsys, monkeypatch):

    def faketags(tags):
        pass
    monkeypatch.setattr(ddl.asset_exploration, "print_tags", faketags)

    component = ComponentAsset({"name": "test",
                                "id": "test_id",
                                "parts": [{"type": "image",
                                           "image_id": "image"},
                                          {"type": "component",
                                           "component_id": "component"}],
                                "tags": []},
                               "test")
    ddl.asset_exploration.print_component_info(component)
    captured = capsys.readouterr()
    assert captured.out == """Component name: test
Component ID: test_id
Number of parts: 2
"""
