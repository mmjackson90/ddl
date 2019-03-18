from ddl.cli import validate_assetpack, main
from click.testing import CliRunner


def test_validate_assetpack():
    runner = CliRunner()
    result = runner.invoke(main, ["validate-assetpack", "assetpacks/example_isometric"])
    assert result.exit_code == 0
    assert result.output == """Pack validated
Images validated
Components validated
Validation passed. assetpacks/example_isometric is a good assetpack.
"""
