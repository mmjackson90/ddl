"""Test the CLI utils"""

from ddl.cli_utils import get_asset_choices
from tests.test_asset_exploration import get_test_assetpack


def test_get_asset_choices():
    """Tests asset choices are correctly pulled out"""
    assetpack = get_test_assetpack()
    choices = get_asset_choices(assetpack)
    assert choices[0] == 'Back'
    assert choices[2] == 'Component: test.a'
    assert choices[3] == 'Component: test.b'
    assert choices[5] == 'Image: test.c'
