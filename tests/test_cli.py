"""Tests the non-interactive functions of the CLI tool using click's runner"""

import ddl.cli
from ddl.cli import main, init_component

from ddl.assetpack import Assetpack
from ddl.asset import ComponentAsset
from click.testing import CliRunner
from test_asset_exploration import get_test_assetpack


# Yes, it's a global in a test suite. No, I don't feel bad about using it.
PROMPT_CALLS = 0


def test_validate_assetpack():
    """Tests that an assetpack validates correctly"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """Pack validated
Images validated
Components validated
Validation passed. assetpacks/example_isometric is a good assetpack.
"""


def test_assetpack_filefail():
    """Tests that an assetpack fails if files arent available"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "does-not-exist"])
    assert result.exit_code == 0
    assert result.output == """

########ERROR########
does-not-exist/pack.json was not found.


########ERROR########
does-not-exist/images.json was not found.


########ERROR########
does-not-exist/components.json was not found.
"""


def test_assetpack_invalid():
    """Tests that an assetpack fails if a file doesnt validate"""
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_json_fail"])
    assert result.exit_code == 0
    assert result.output == """

########ERROR########
'projection' is a required property


########ERROR########
'name' is a required property


########ERROR########
Additional properties are not allowed ('grid' was unexpected)
"""


def test_explore_projection_info(monkeypatch):
    """Tests that pack info can be properly pulled out"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        global PROMPT_CALLS
        choices = ['See pack information', 'See projection information', 'Quit']
        result = {'init': choices[PROMPT_CALLS]}
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    result = runner.invoke(main, ["explore-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """
Name: Example Isometric Asset Pack
Author: The Easy Dungeon Company
Projection: isometric
Tags:
    example


Type: Isometric
Grid height: 170 pixels.
Grid width: 294 pixels.



"""


def test_explore_assetpack(monkeypatch):
    """Tests that pack info can be properly pulled out"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeshow_pack_info(assetpack):
        print("""Called show_pack_info successfully""")

    def fakeshow_projection_info(assetpack):
        print("""Called show_projection_info successfully""")

    def fakeexplore_assets(assetpack):
        print("""Called explore_assets successfully""")

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
        global PROMPT_CALLS
        choices = [
            'See pack information',
            'See projection information',
            'Explore Assets',
            'Quit'
        ]
        result = {'init': choices[PROMPT_CALLS]}
        PROMPT_CALLS = PROMPT_CALLS+1
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    monkeypatch.setattr(ddl.cli, "show_projection_info", fakeshow_projection_info)
    monkeypatch.setattr(ddl.cli, "show_pack_info", fakeshow_pack_info)
    monkeypatch.setattr(ddl.cli, "explore_assets", fakeexplore_assets)
    result = runner.invoke(main, ["explore-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """
Called show_pack_info successfully


Called show_projection_info successfully


Called explore_assets successfully



"""


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
        choices = ['test name', 'test-id', ['tag']]
        result = {}
        for question, choice in zip(component_info, choices):
            result[question['name']] = choice
        return result

    monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
    assert ddl.cli.get_initial_component_info(assetpack) == {'component_name': 'test name',
                                                             'component_id': 'test-id',
                                                             'component_tags': ['tag']}
