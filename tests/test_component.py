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
