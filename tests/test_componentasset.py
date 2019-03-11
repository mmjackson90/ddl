"""
Tests Components
"""

from ddl.asset import ComponentAsset


def test_component_init():
    """Tests the initialisation of components"""
    data = {
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
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 0,
                "y": 1
            }
        ],
        "tags": [
            "example"
        ]
    }
    component = ComponentAsset(data, 'test_assetpack_name')
    if not component.assetpack_name == 'test_assetpack_name':
        raise AssertionError()
    if not component.data == data:
        raise AssertionError()
    if not len(component.parts) == 2:
        raise AssertionError()


def test_rescale_component():
    """Tests that components rescale correctly when asked"""
    data = {
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
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 2,
                "y": 3
            }
        ],
        "tags": [
            "example"
        ]
    }
    component = ComponentAsset(data, 'test_assetpack_name')
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
    data = {
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
    }
    component = ComponentAsset(data, 'test_assetpack_name')
    parts = component.get_part_list(2, 3)
    type, name, offset_x, offset_y = parts[0]
    if not type == "image":
        raise AssertionError()
    if not name == "test_assetpack_name.floor-1x1-exact":
        raise AssertionError()
    if not offset_x == 2:
        raise AssertionError()
    if not offset_y == 3:
        raise AssertionError()
    type, name, offset_x, offset_y = parts[1]
    if not type == "component":
        raise AssertionError()
    if not name == "test_assetpack_name.test-component-thing":
        raise AssertionError()
    if not offset_x == 4:
        raise AssertionError()
    if not offset_y == 6:
        raise AssertionError()
