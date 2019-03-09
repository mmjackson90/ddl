"""
Tests Components
"""

from ddl import Component


def test_component_init():
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
    component = Component(data, 'test_assetpack_name')
    if not component.assetpack_name == 'test_assetpack_name':
        raise AssertionError()
    if not component.data == data:
        raise AssertionError()
    if not len(component.parts) == 2:
        raise AssertionError()


def test_rescale_component():
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
    component = Component(data, 'test_assetpack_name')
    component.rescale(2, 3)
    if not component.data["parts"][0]["x"] == 0:
        raise AssertionError()
    if not component.data["parts"][0]["y"] == 0:
        raise AssertionError()
    if not component.data["parts"][1]["x"] == 1:
        raise AssertionError()
    if not component.data["parts"][1]["y"] == 1:
        raise AssertionError()


def test_get_location_list():
