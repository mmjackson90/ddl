"""Tests the asset exploration functions of the CLI (which are interactive)
These are deliberately part-integration rather than unit, as the important thing for the
CLI is that the methods be called consistently."""

import ddl.asset_exploration
from ddl.assetpack import Assetpack
from ddl.asset import ImageAsset, ComponentAsset
from ddl.projection import IsometricProjection


def get_test_assetpack():
    """Loads up a semi-fake assetpack"""
    projection = IsometricProjection(10, 20)
    assetpack = Assetpack('test', projection)
    images = [
             {
                 "name": "1x1 Floor low_res",
                 "id": "c",
                 "image": "1x1_floor_low_res.png",
                 "top_left": {
                     "x": 73,
                     "y": 0
                 }
             }
           ]
    for image in images:
        new_image = ImageAsset(image,
                               assetpack_id='test',
                               assetpack_path='assetpacks/low_res_isometric'
                               )
        assetpack.add_image(new_image)
    components = [
             {
                 "name": "test Floor low_res",
                 "id": "a",
                 "parts": [
                     {
                         "type": "image",
                         "image_id": "c",
                         "x": 0,
                         "y": 0
                     },
                     {
                         "type": "image",
                         "image_id": "c",
                         "x": 1,
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
                         "image_id": "c",
                         "x": 0,
                         "y": 0
                     }
                 ],
                 "tags": [
                     "example"
                 ]
             }
         ]
    for component in components:
        new_component = ComponentAsset(component, assetpack_id='test')
        assetpack.taglist.add_component(new_component)
        assetpack.add_component(new_component)
    return assetpack


def test_show_pack_info(capsys):
    """Tests pack info displays correctly"""
    # Mostly this is to test that capsys and monkeypatch work the way I expect.
    ddl.asset_exploration.show_pack_info('assetpacks/example_isometric')
    captured = capsys.readouterr()
    assert captured.out == """Name: Example Isometric Asset Pack
Author: The Easy Dungeon Company
Projection: isometric
Tags:
    example
"""


class VariableStore:
    """Simple store for variables"""


def test_show_projection_isometric(capsys, monkeypatch):
    """Tests projection info displays correctly"""
    assetpack = VariableStore()
    assetpack.projection = VariableStore()
    assetpack.projection.height = 20
    assetpack.projection.width = 10
    monkeypatch.setattr(ddl.asset_exploration, "IsometricProjection", VariableStore)
    ddl.asset_exploration.show_projection_info(assetpack)
    captured = capsys.readouterr()
    assert captured.out == """Type: Isometric
Grid height: 20 pixels.
Grid width: 10 pixels.
"""


def test_show_projection_topdown(capsys):
    """Tests projection info displays correctly"""

    assetpack = VariableStore()
    assetpack.projection = VariableStore()
    assetpack.projection.height = 20
    assetpack.projection.width = 10
    ddl.asset_exploration.show_projection_info(assetpack)
    captured = capsys.readouterr()
    assert captured.out == """Type: Top Down
Grid height: 20 pixels.
Grid width: 10 pixels.
"""


def test_print_image_info(capsys):
    """Tests image info prints"""
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


def test_print_component_info(capsys):
    """Tests component info prints"""
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


def test_show_component():
    """Functional test. No asserts, just makes sure it doesn't bork."""
    assetpack = get_test_assetpack()
    ddl.asset_exploration.show_component(assetpack, assetpack.components['test.a'])


def test_get_asset_component():
    """Tests a component asset is correctly pulled based on choices"""
    assetpack = get_test_assetpack()
    asset = ddl.asset_exploration.get_asset(assetpack, "Component: test.a")
    assert isinstance(asset, ComponentAsset)


def test_get_asset_image():
    """Tests a component asset is correctly pulled based on choices"""
    assetpack = get_test_assetpack()
    asset = ddl.asset_exploration.get_asset(assetpack, "Image: test.c")
    assert isinstance(asset, ImageAsset)


PROMPT_CALLS = 0


def test_explore_assets(monkeypatch):
    """Tests the explore assets loop"""

    global PROMPT_CALLS
    PROMPT_CALLS = 0

    class FakeAssetpack:
        """A fake assetpack for storing results"""
        def __init__(self):
            self.option_chosen = ''
            self.options = ['a', 'b', 'c']

    def fake_get_choices(assetpack):
        """gives some fake choices to choose from"""
        return assetpack.options

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        assert style is not None
        global PROMPT_CALLS
        choices = [
            {'choices': 'a'},
            {'choices': 'Back'}
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    def fake_explore_assets(option_chosen, assetpack):
        """Not a real function"""
        assetpack.option_chosen = option_chosen

    assetpack = FakeAssetpack()
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    monkeypatch.setattr(ddl.asset_exploration, "get_asset_choices", fake_get_choices)
    monkeypatch.setattr(ddl.asset_exploration, "explore_asset", fake_explore_assets)

    ddl.asset_exploration.explore_assets(assetpack)
    assert assetpack.option_chosen == 'a'


class FakeAsset:
    """Not a real asset"""
    def __init__(self, name):
        self.name = name

    def show(self):
        """Sets a flag"""
        global ASSET_SHOWN
        ASSET_SHOWN = True


def fake_get_asset(assetpack, initial_option):
    """Returns a fake asset"""
    return FakeAsset(assetpack + initial_option)


def fake_show_component(assetpack, asset):
    """Sets a flag"""
    assert assetpack is not None
    assert asset is not None
    global ASSET_SHOWN
    ASSET_SHOWN = True


def fake_print_info(asset):
    """Sets a flag"""
    assert asset is not None
    global ASSET_PRINTED
    ASSET_PRINTED = True


ASSET_SHOWN = False
ASSET_PRINTED = False


def test_explore_show_image(monkeypatch):
    """Tests that showing an image works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "ImageAsset", FakeAsset)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show image"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_SHOWN
    ASSET_SHOWN = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_SHOWN


def test_explore_show_component(monkeypatch):
    """Tests that showing a component works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "show_component", fake_show_component)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show image"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_SHOWN
    ASSET_SHOWN = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_SHOWN


def test_explore_print_image(monkeypatch):
    """Tests that printing image metadata works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "ImageAsset", FakeAsset)
    monkeypatch.setattr(ddl.asset_exploration, "print_image_info", fake_print_info)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show metadata"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_PRINTED
    ASSET_PRINTED = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_PRINTED


def test_explore_print_component(monkeypatch):
    """Tests that printing component metadata works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "print_component_info", fake_print_info)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show metadata"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_PRINTED
    ASSET_PRINTED = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_PRINTED


def test_explore_both_image(monkeypatch):
    """Tests that doing both things works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "ImageAsset", FakeAsset)
    monkeypatch.setattr(ddl.asset_exploration, "print_image_info", fake_print_info)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show both"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_PRINTED
    ASSET_PRINTED = False
    global ASSET_SHOWN
    ASSET_SHOWN = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_PRINTED
    assert ASSET_SHOWN


def test_explore_both_component(monkeypatch):
    """Tests that doing both things works"""
    monkeypatch.setattr(ddl.asset_exploration, "get_asset", fake_get_asset)
    monkeypatch.setattr(ddl.asset_exploration, "print_component_info", fake_print_info)
    monkeypatch.setattr(ddl.asset_exploration, "show_component", fake_show_component)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        return {"choices": "Show both"}
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    global ASSET_PRINTED
    ASSET_PRINTED = False
    global ASSET_SHOWN
    ASSET_SHOWN = False
    ddl.asset_exploration.explore_asset('a', 'b')
    assert ASSET_PRINTED
    assert ASSET_SHOWN
