"""Tests the non-interactive functions of the CLI tool using click's runner"""

import ddl.cli
from ddl.cli import main, init_component

from ddl.asset import ComponentAsset
from click.testing import CliRunner
from test_asset_exploration import get_test_assetpack


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
    """Tests that an assetpack validates correctly"""
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
    """Tests that an assetpack validates correctly"""
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
