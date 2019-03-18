"""Tests the asset exploration functions of """

import ddl.asset_exploration
from ddl.projection import IsometricProjection, TopDownProjection


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
    class FakeAssetPack:
        def __init__(self, projection):
            self.projection = projection

    ddl.asset_exploration.show_projection_info(FakeAssetPack(IsometricProjection(10, 20)))
    captured = capsys.readouterr()
    assert captured.out == """Type: Isometric
Grid height: 20 pixels.
Grid width: 10 pixels.
"""


def test_get_asset_choices(capsys, monkeypatch):
    class FakeAssetPack:
        def __init__(self):
            self.components = {"a": 1,
                               "b": 1}
            self.images = {"c": 1}
    choices = ddl.asset_exploration.get_asset_choices(FakeAssetPack())
    assert choices[0] == 'Back'
    assert choices[2] == 'Component: a'
    assert choices[3] == 'Component: b'
    assert choices[5] == 'Image: c'
