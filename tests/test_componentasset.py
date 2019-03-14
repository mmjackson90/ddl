"""
Tests Components
"""

from ddl.asset import ComponentAsset


class FakeImageAsset():
    "A fake image asset that does nothing but return a test ID"
    def __init__(self):
        self.asset_id = 'test_image'

    def get_full_id(self):
        return("test.test_image")


class FakeComponentAsset():
    "A fake component asset that does nothing but return a test ID"
    def __init__(self):
        self.asset_id = 'test_component'

    def get_full_id(self):
        return("test.test_component")


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
    return(ComponentAsset(data, 'test_assetpack_name'))


def test_component_init():
    """Tests the initialisation of components"""
    component = get_test_component()
    if not component.assetpack_name == 'test_assetpack_name':
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


def test_get_part_list():
    """Tests that components get their parts list correctly when asked"""
    component = get_test_component()
    parts = component.get_part_list(2, 3)
    asset_type, name, offset_x, offset_y = parts[0]
    if not asset_type == "image":
        raise AssertionError()
    if not name == "test_assetpack_name.floor-1x1-exact":
        raise AssertionError()
    if not offset_x == 2:
        raise AssertionError()
    if not offset_y == 3:
        raise AssertionError()
    asset_type, name, offset_x, offset_y = parts[1]
    if not asset_type == "component":
        raise AssertionError()
    if not name == "test_assetpack_name.test-component-thing":
        raise AssertionError()
    if not offset_x == 4:
        raise AssertionError()
    if not offset_y == 6:
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
    data = {
        "name": "2x2 Floor exact",
        "id": "floor-2x2-exact",
        "parts": [
            {"asset_id": "test_assetpack_name.floor-1x1-exact",
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 0,
                "y": 0
             },
            {"asset_id": "test_assetpack_name.test-component-thing",
                "type": "component",
                "component_id": "test-component-thing",
                "x": 2,
                "y": 3
             }
        ],
        "tags": [
            "example"
        ]
    }
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
            "y": 0,
            "asset_id": "test_assetpack_name.floor-1x1-exact"
        },
        {
            "type": "component",
            "component_id": "test-component-thing",
            "x": 2,
            "y": 3,
            "asset_id": "test_assetpack_name.test-component-thing"
        }
    ],
    "tags": [
        "example"
    ]
}"""
    assert component.get_json() == output_string
