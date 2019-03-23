"""Tests the non-interactive functions of the CLI tool using click's runner"""

import ddl.cli
import ddl.image_helper
from ddl.cli import main, init_component, validate_component_id, add_component
import os
from pytest import raises
import PyInquirer
from ddl.asset import ComponentAsset
from click.testing import CliRunner
import ddl.asset_exploration
from test_asset_exploration import get_test_assetpack


# Yes, it's a global in a test suite. No, I don't feel bad about using it.
PROMPT_CALLS = 0


def test_validate_assetpack():
    """Tests that an assetpack validates correctly"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """DDL CLI
Pack validated
Images validated
Components validated
Validation passed. assetpacks/example_isometric is a good assetpack.
"""


def test_assetpack_filefail():
    """Tests that an assetpack fails if files arent available"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "does-not-exist"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
########ERROR########
does-not-exist/pack.json was not found.
########ERROR########
does-not-exist/images.json was not found.
########ERROR########
does-not-exist/components.json was not found."""


def test_assetpack_invalid():
    """Tests that an assetpack fails if a file doesnt validate"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_json_fail"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
########ERROR########
'projection' is a required property
########ERROR########
'name' is a required property
########ERROR########
Additional properties are not allowed ('grid' was unexpected)"""


def test_explore_assetpack(monkeypatch):
    """Tests that pack info options function properly
    Mostly a test of prompt monkeypatching, but improves unit testing some."""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        assert style is not None
        global PROMPT_CALLS
        choices = [
            {'choices': 'See pack information'},
            {'choices': 'See projection information'},
            {'choices': 'Explore Assets'},
            {'choices': 'Component: easy-dungeon-ddl-example-iso.floor-1x1-exact'},
            {'choices': 'Show both'},
            {'choices': 'Image: easy-dungeon-ddl-example-iso.floor-1x1-exact'},
            {'choices': 'Show both'},
            {'choices': 'Back'},
            {'choices': 'Quit'}
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    monkeypatch.setattr(ddl.asset_exploration, "prompt", fakeprompt)
    result = runner.invoke(main, ["explore-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
Name: Example Isometric Asset Pack
Author: The Easy Dungeon Company
Projection: isometric
Tags:
    example
Type: Isometric
Grid height: 170 pixels.
Grid width: 294 pixels.
Component name: 1x1 Floor Exact
Component ID: floor-1x1-exact
Tags:
    example
    floor
Number of parts: 1
Image name: 1x1 Floor exact
Image ID: floor-1x1-exact
Grid Top Left Corner pixel (x): 148
Grid Top Left Corner pixel (y): 0"""


def test_add_component(monkeypatch):
    """Tests that assets can be added to components OK."""
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    assetpack = get_test_assetpack()
    data = {
        "name": 'Test',
        "id": 'test-part',
        "parts": [],
        "tags": []
    }
    component = ComponentAsset(data, assetpack)

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        if style is None:
            raise AssertionError()
        global PROMPT_CALLS
        if PROMPT_CALLS == 0:
            result = {'x': 1, 'y': 2.1}
        else:
            result = {'x': 3.1, 'y': 5}
        PROMPT_CALLS = PROMPT_CALLS + 1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)

    add_component("Image: test.c", component, assetpack)
    add_component("Component: test.a", component, assetpack)

    assert component.parts == [{'type': 'image', 'image_id': 'c', 'asset_id': 'test.c', 'x': 1.0, 'y': 2.1},
                               {'type': 'component', 'component_id': 'a', 'asset_id': 'test.a', 'x': 3.1, 'y': 5.0}]


def test_validate_component_id():
    """test a valid component ID is allowed through"""
    assetpack = get_test_assetpack()
    assert validate_component_id('brand_new', assetpack) is True


def test_validate_id_too_short():
    """test a short component ID is rejected"""
    assetpack = get_test_assetpack()
    with raises(PyInquirer.ValidationError):
        assert validate_component_id('z', assetpack) is False


def test_validate_component_exists():
    """Test an in use component ID is rejected"""
    assetpack = get_test_assetpack()
    assetpack.add_component(ComponentAsset({
        "name": 'thing',
        "id": 'thing',
        "parts": [],
        "tags": []
    }, assetpack))
    with raises(PyInquirer.ValidationError):
        assert validate_component_id('thing', assetpack) is False


def test_init_component():
    """Tests that blank components are initialised properly based on user input"""
    assetpack = get_test_assetpack()
    info = {"component_name": "test",
            "component_id": "test_id",
            "component_tags": "a,b"}

    component = init_component(assetpack, info)
    assert isinstance(component, ComponentAsset)
    assert component.name == "test"
    assert component.asset_id == "test_id"
    assert component.tags == ["a", "b"]
    assert component.parts == []


def test_initial_component_info(monkeypatch):
    """A quick try to monkeypatch prompt again"""
    assetpack = get_test_assetpack()

    def fakeprompt(component_info, style):
        """A fake prompt function that does *something* with tags"""
        assert style is not None
        choices = ['test name', 'test-id', ['tag']]
        result = {}
        for question, choice in zip(component_info, choices):
            result[question['name']] = choice
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    assert ddl.cli.get_initial_component_info(assetpack) == {'component_name': 'test name',
                                                             'component_id': 'test-id',
                                                             'component_tags': ['tag']}


def test_create_new_component(monkeypatch):
    """FUNCTIONALTests that components can be created neatly"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        assert style is not None
        global PROMPT_CALLS
        choices = [
            {'component_name': 'Test name',
             'component_id': 'test-id',
             'component_tags': 'thing, stuff,nonsense'},
            {'choice': 'Add an asset'},
            {'explore': 'Component: easy-dungeon-ddl-example-iso.floor-1x1-exact'},
            {'x': 1, 'y': 2},
            {'choice': 'Add an asset'},
            {'explore': 'Component: easy-dungeon-ddl-example-iso.floor-1x1-exact'},
            {'x': 3, 'y': 5},
            {'choice': 'Undo'},
            {'choice': 'Done'}
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    result = runner.invoke(main, ["create-new-component", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
{
    "name": "Test name",
    "id": "test-id",
    "parts": [
        {
            "type": "component",
            "component_id": "floor-1x1-exact",
            "x": 1.0,
            "y": 2.0
        }
    ],
    "tags": [
        "thing",
        "stuff",
        "nonsense"
    ]
}"""


def test_create_new_images_iso(monkeypatch):
    """FUNCTIONALTests that components can be created neatly"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        assert style is not None
        global PROMPT_CALLS
        choices = [
            {'next_action': 'Edit offset X'},
            {'x': '152'},
            {'next_action': 'Edit offset Y'},
            {'y': '6'},
            {'next_action': 'Next'},
            {'id': 'test',
             'name': 'Test name'},
            {'next_action': 'Skip'},
            {'next_action': 'Quit now'},
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    monkeypatch.setattr(ddl.image_helper, "prompt", fakeprompt)
    result = runner.invoke(main, ["create-new-images",
                                  "--gridtype", "isometric",
                                  "--width", "290",
                                  "--height", "170",
                                  "assetpacks/example_isometric/art"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
{
    "images": [
        {
            "name": "Test name",
            "id": "test",
            "image": "1_wall_exact.png",
            "top_left": {
                "x": 152,
                "y": 6
            }
        }
    ]
}"""


def test_create_new_images_topdown(monkeypatch):
    """FUNCTIONALTests that components can be created neatly"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        assert style is not None
        global PROMPT_CALLS
        choices = [
            {'next_action': 'Edit offset X'},
            {'x': '152'},
            {'next_action': 'Edit offset Y'},
            {'y': '6'},
            {'next_action': 'Next'},
            {'id': 'test',
             'name': 'Test name'},
            {'next_action': 'Skip'},
            {'next_action': 'Quit now'},
        ]
        result = choices[PROMPT_CALLS]
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    monkeypatch.setattr(ddl.image_helper, "prompt", fakeprompt)
    result = runner.invoke(main, ["create-new-images",
                                  "--gridtype", "topdown",
                                  "--width", "290",
                                  "--height", "170",
                                  "assetpacks/example_isometric/art"])
    assert result.exit_code == 0
    assert os.linesep.join([s for s in result.output.splitlines() if s]) == """DDL CLI
{
    "images": [
        {
            "name": "Test name",
            "id": "test",
            "image": "1_wall_exact.png",
            "top_left": {
                "x": 152,
                "y": 6
            }
        }
    ]
}"""
