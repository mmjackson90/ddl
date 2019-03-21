"""Tests the non-interactive functions of the CLI tool using click's runner"""

import ddl.cli
import ddl.image_helper
from ddl.cli import main, init_component, validate_component_id, add_component

from pytest import raises
import PyInquirer
from ddl.assetpack import Assetpack
from ddl.asset import ComponentAsset
from click.testing import CliRunner
import ddl.asset_exploration
from test_asset_exploration import get_test_assetpack


# Yes, it's a global in a test suite. No, I don't feel bad about using it.
PROMPT_CALLS = 0

#
# def test_validate_assetpack():
#     """Tests that an assetpack validates correctly"""
#     runner = CliRunner()
#     result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_isometric"])
#     assert result.exit_code == 0
#     assert result.output == """Pack validated
# Images validated
# Components validated
# Validation passed. assetpacks/example_isometric is a good assetpack.
# """
#
#
# def test_assetpack_filefail():
#     """Tests that an assetpack fails if files arent available"""
#     runner = CliRunner()
#     result = runner.invoke(main, ["validate-assetpack", "does-not-exist"])
#     assert result.exit_code == 0
#     assert result.output == """
#
# ########ERROR########
# does-not-exist/pack.json was not found.
#
#
# ########ERROR########
# does-not-exist/images.json was not found.
#
#
# ########ERROR########
# does-not-exist/components.json was not found.
# """
#
#
# def test_assetpack_invalid():
#     """Tests that an assetpack fails if a file doesnt validate"""
#     runner = CliRunner()
#     result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_json_fail"])
#     assert result.exit_code == 0
#     assert result.output == """
#
# ########ERROR########
# 'projection' is a required property
#
#
# ########ERROR########
# 'name' is a required property
#
#
# ########ERROR########
# Additional properties are not allowed ('grid' was unexpected)
# """
#
#
# def test_explore_assetpack(monkeypatch):
#     """Tests that pack info options function properly
#     Mostly a test of prompt monkeypatching, but improves unit testing some."""
#     runner = CliRunner()
#     global PROMPT_CALLS
#     PROMPT_CALLS = 0
#
#     def fakeshow_pack_info(assetpack):
#         print("""Called show_pack_info successfully""")
#
#     def fakeshow_projection_info(assetpack):
#         print("""Called show_projection_info successfully""")
#
#     def fakeexplore_assets(assetpack):
#         print("""Called explore_assets successfully""")
#
#     def fakeprompt(choices, style):
#         """A fake prompt function that returns a response"""
#         global PROMPT_CALLS
#         choices = [
#             'See pack information',
#             'See projection information',
#             'Explore Assets',
#             'Quit'
#         ]
#         result = {'choices': choices[PROMPT_CALLS]}
#         PROMPT_CALLS = PROMPT_CALLS+1
#         return result
#
#     monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
#     monkeypatch.setattr(ddl.cli, "show_projection_info", fakeshow_projection_info)
#     monkeypatch.setattr(ddl.cli, "show_pack_info", fakeshow_pack_info)
#     monkeypatch.setattr(ddl.cli, "explore_assets", fakeexplore_assets)
#     result = runner.invoke(main, ["explore-assetpack", "assetpacks/example_isometric"])
#     assert result.exit_code == 0
#     assert result.output == """
# Called show_pack_info successfully
#
#
# Called show_projection_info successfully
#
#
# Called explore_assets successfully
#
#
#
# """
#
#
# def test_add_component(monkeypatch):
#     """Tests that assets can be added to components OK."""
#     global PROMPT_CALLS
#     PROMPT_CALLS = 0
#
#     assetpack = get_test_assetpack()
#     data = {
#         "name": 'Test',
#         "id": 'test-part',
#         "parts": [],
#         "tags": []
#     }
#     component = ComponentAsset(data, assetpack.pack_id)
#
#     def fakeprompt(choices, style):
#         """A fake prompt function that returns a response"""
#         global PROMPT_CALLS
#         if PROMPT_CALLS == 0:
#             result = {'x': 1, 'y': 2.1}
#         else:
#             result = {'x': 3.1, 'y': 5}
#         PROMPT_CALLS = PROMPT_CALLS + 1
#         return result
#
#     monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
#
#     add_component("Image: test.c", component, assetpack)
#     add_component("Component: test.a", component, assetpack)
#
#     assert component.parts == [{'type': 'image', 'image_id': 'c', 'asset_id': 'test.c', 'x': 1.0, 'y': 2.1},
#                                {'type': 'component', 'component_id': 'a', 'asset_id': 'test.a', 'x': 3.1, 'y': 5.0}]
#
#
# def test_validate_component_id():
#     assetpack = get_test_assetpack()
#     assert validate_component_id('brand_new', assetpack) is True
#
#
# def test_validate_id_too_short():
#     assetpack = get_test_assetpack()
#     with raises(PyInquirer.ValidationError):
#         assert validate_component_id('z', assetpack) is False
#
#
# def test_validate_component_exists():
#     assetpack = get_test_assetpack()
#     assetpack.add_component(ComponentAsset({
#         "name": 'thing',
#         "id": 'thing',
#         "parts": [],
#         "tags": []
#     }, assetpack.pack_id))
#     with raises(PyInquirer.ValidationError):
#         assert validate_component_id('thing', assetpack) is False
#
#
# def test_init_component():
#     """Tests that blank components are initialised properly based on user input"""
#     assetpack = get_test_assetpack()
#     info = {"component_name": "test",
#             "component_id": "test_id",
#             "component_tags": "a,b"}
#
#     component = init_component(assetpack, info)
#     assert isinstance(component, ComponentAsset)
#     assert component.name == "test"
#     assert component.asset_id == "test_id"
#     assert component.tags == ["a", "b"]
#     assert component.parts == []
#
#
# def test_initial_component_info(monkeypatch):
#     """A quick try to monkeypatch prompt again"""
#     assetpack = get_test_assetpack()
#
#     def fakeprompt(component_info, style):
#         """A fake prompt function that does *something* with tags"""
#         choices = ['test name', 'test-id', ['tag']]
#         result = {}
#         for question, choice in zip(component_info, choices):
#             result[question['name']] = choice
#         return result
#
#     monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
#     assert ddl.cli.get_initial_component_info(assetpack) == {'component_name': 'test name',
#                                                              'component_id': 'test-id',
#                                                              'component_tags': ['tag']}
#
#
# def test_create_new_component(monkeypatch):
#     """FUNCTIONALTests that components can be created neatly"""
#     runner = CliRunner()
#     global PROMPT_CALLS
#     PROMPT_CALLS = 0
#
#     def fakeprompt(choices, style):
#         """A fake prompt function that returns a response"""
#         global PROMPT_CALLS
#         choices = [
#             {'component_name': 'Test name',
#              'component_id': 'test-id',
#              'component_tags': 'thing, stuff,nonsense'},
#             {'choice': 'Add an asset'},
#             {'explore': 'Component: easy-dungeon-ddl-example-iso.floor-1x1-exact'},
#             {'x': 1, 'y': 2},
#             {'choice': 'Done'}
#         ]
#         result = choices[PROMPT_CALLS]
#         PROMPT_CALLS = PROMPT_CALLS+1
#         return result
#
#     monkeypatch.setattr(ddl.cli, "prompt", fakeprompt)
#     result = runner.invoke(main, ["create-new-component", "assetpacks/example_isometric"])
#     assert result.exit_code == 0
#     assert result.output == """
#
#
# {
#     "name": "Test name",
#     "id": "test-id",
#     "parts": [
#         {
#             "type": "component",
#             "component_id": "floor-1x1-exact",
#             "x": 1.0,
#             "y": 2.0
#         }
#     ],
#     "tags": [
#         "thing",
#         "stuff",
#         "nonsense"
#     ]
# }
# """


def test_create_new_images_iso(monkeypatch):
    """FUNCTIONALTests that components can be created neatly"""
    runner = CliRunner()
    global PROMPT_CALLS
    PROMPT_CALLS = 0

    def fakeprompt(choices, style):
        """A fake prompt function that returns a response"""
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
    assert result.output.strip() == """{
    "images": [
        {
            "name": "Test name",
            "id": "test",
            "image": "1x1_floor_fuzzy.png",
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
    assert result.output.strip() == """{
    "images": [
        {
            "name": "Test name",
            "id": "test",
            "image": "1x1_floor_fuzzy.png",
            "top_left": {
                "x": 152,
                "y": 6
            }
        }
    ]
}"""
