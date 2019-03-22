"""
Tests Components
"""

from ddl.asset import ComponentAsset
import json
from jsonschema import validate
from ddl.assetpack import AssetpackFactory


class FakeImageAsset():
    "A fake image asset that does nothing but return a test ID"
    def __init__(self):
        self.asset_id = 'test_image'

    def get_full_id(self):
        """returns a fake ID string"""
        return("test."+self.asset_id)


class FakeComponentAsset():
    "A fake component asset that does nothing but return a test ID"
    def __init__(self):
        self.asset_id = 'test_component'

    def get_full_id(self):
        """returns a fake ID string"""
        return("test."+self.asset_id)


class FakeAssetpack():
    """The fakest assetpack around"""
    def __init__(self):
        self.pack_id = 'test_assetpack_name'


def get_test_data():
    """returns some test data"""
    return({
        "name": "2x2 Floor exact",
        "id": "floor-2x2-exact",
        "parts": [
            {
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 0,
                "y": 0
            },
            {
                "type": "component",
                "component_id": "test-component-thing",
                "x": 2,
                "y": 3
            }
        ],
        "tags": [
            "example"
        ]
    })


def get_test_component():
    "Sets up a new component with some test data."
    data = get_test_data()
    return(ComponentAsset(data, FakeAssetpack()))


def test_component_init():
    """Tests the initialisation of components"""
    component = get_test_component()
    if not component.assetpack_id == 'test_assetpack_name':
        raise AssertionError()
    if not len(component.parts) == 2:
        raise AssertionError()


def test_rescale_component():
    """Tests that components rescale correctly when asked"""
    component = get_test_component()
    component.rescale(2, 3)
    if not component.data["parts"][0]["x"] == 0:
        raise AssertionError()
    if not component.data["parts"][0]["y"] == 0:
        raise AssertionError()
    if not component.data["parts"][1]["x"] == 1:
        raise AssertionError()
    if not component.data["parts"][1]["y"] == 1:
        raise AssertionError()


def test_get_add_image():
    """tests that images add to the component correctly"""
    component = get_test_component()
    component.add_image(FakeImageAsset(), 1, 2)
    assert len(component.parts) == 3
    values = component.parts[2].values()
    asset_type, name, offset_x, offset_y, asset_id = values
    assert asset_type == "image"
    assert name == "test_image"
    assert offset_x == 1
    assert offset_y == 2
    assert asset_id == "test.test_image"


def test_add_component():
    """Tests that components add to the component correctly"""
    component = get_test_component()
    component.add_component(FakeComponentAsset(), 1, 2)
    assert len(component.parts) == 3
    values = component.parts[2].values()
    asset_type, name, offset_x, offset_y, asset_id = values
    assert asset_type == "component"
    assert name == "test_component"
    assert offset_x == 1
    assert offset_y == 2
    assert asset_id == "test.test_component"


def test_remove_last_part():
    """Tests that the last part added can be removed"""
    component = get_test_component()
    component.remove_last_part()
    assert len(component.parts) == 1
    values = component.parts[0].values()
    asset_type, name, offset_x, offset_y, asset_id = values
    assert asset_type == "image"
    assert name == "floor-1x1-exact"
    assert offset_x == 0
    assert offset_y == 0
    assert asset_id == "test_assetpack_name.floor-1x1-exact"


def test_get_component_data():
    """Tests that the component data as a dict returns OK"""
    component = get_test_component()
    data = get_test_data()
    assert component.get_data() == data


def test_get_component_json():
    """tests that the component prints it's json correctly"""
    component = get_test_component()
    output_string = """\
{
    "name": "2x2 Floor exact",
    "id": "floor-2x2-exact",
    "parts": [
        {
            "type": "image",
            "image_id": "floor-1x1-exact",
            "x": 0,
            "y": 0
        },
        {
            "type": "component",
            "component_id": "test-component-thing",
            "x": 2,
            "y": 3
        }
    ],
    "tags": [
        "example"
    ]
}"""
    assert component.get_json() == output_string


def test_json_validity():
    """
    tests that the component prints it's json in a way that is
    valid for later loading.
    """
    component = get_test_component()
    component_json = component.get_json()
    output_json = json.loads(
        f"""
        {{
                "components": [
                    {component_json}
                ]
            }}
        """
    )
    with open('schemas/components.json') as schema_file:
        schema_json = json.load(schema_file)
        validate(output_json, schema_json)


def test_simple_image_location_list():
    """Tests an assetpack will return an imagelocationlist for a simple
    component if asked. No Nesting."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component = assetpack.components['easy-dungeon-ddl-example-iso.floor-wall-exact']
    ill = component.get_image_location_list(2, 3)
    if len(ill) != 2:
        raise AssertionError()
    # Required to check things are ending up in the right places in the list
    if not ill[0][0].asset_id == "floor-1x1-exact":
        raise AssertionError(ill[0][0].asset_id)
    if not ill[1][0].asset_id == "exact-wall-1":
        raise AssertionError()


def test_nested_image_location_list():
    """Tests an assetpack will return an imagelocationlist for a complex
    component if asked. Nesting involved."""
    assetpack = AssetpackFactory.load('assetpacks/example_isometric')
    component = assetpack.components['easy-dungeon-ddl-example-iso.nested-component-test']
    ill = component.get_image_location_list(2, 3)
    if len(ill) != 3:
        raise AssertionError()
    # Required to check things are ending up in the right places in the list
    if not ill[0][0].asset_id == "floor-1x1-exact":
        raise AssertionError(ill[0][0].asset_id)
    if not ill[1][0].asset_id == "exact-wall-1":
        raise AssertionError()
    if not ill[2][0].asset_id == "floor-1x1-fuzzy":
        raise AssertionError()
    # Required to check recursive offsets are being correctly propagated
    assert ill[0][1] == 2
    if not ill[0][2] == 3:
        raise AssertionError()
    if not ill[2][1] == 5:
        raise AssertionError()
    if not ill[2][2] == 4:
        raise AssertionError()
