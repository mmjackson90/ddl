"""
Tests Components
"""

from ddl.asset import ComponentAsset


class FakeImageAsset:
    """A fake imageasset class"""
    def __init__(self, image):
        self.image = image

    def get_image_location_list(self, offset_x, offset_y, *args):
        """Fakes the get_image_location_list method for images"""
        return ([(self.image, offset_x, offset_y)])


class FakeAssetPack():
    """A fake asset pack class"""
    def __init__(self, assets):
        self.assets = assets


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


def test_simple_image_location_list():
    """Tests an image will return an imagelocationlist for itself if asked.
    No Nesting."""
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
    assets = {"test_assetpack_name.i.floor-1x1-exact":
              FakeImageAsset('imageOne')}
    fake_asset_pack = FakeAssetPack(assets)
    component = ComponentAsset(data, 'test_assetpack_name')
    ill = component.get_image_location_list(2, 3, fake_asset_pack)
    if len(ill) != 2:
        raise AssertionError()
    returned_image, offset_x, offset_y = ill[0]
    if not returned_image == 'imageOne':
        raise AssertionError()
    if not offset_x == 2:
        raise AssertionError()
    if not offset_y == 3:
        raise AssertionError()
    returned_image, offset_x, offset_y = ill[1]
    if not returned_image == 'imageOne':
        raise AssertionError()
    if not offset_x == 4:
        raise AssertionError()
    if not offset_y == 6:
        raise AssertionError()


def test_nested_image_location_list():
    """Tests an image will return an imagelocationlist for itself if asked.
    Nesting happens."""
    data_leaf = {
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

    data_branch = {
        "name": "upper Floor exact",
        "id": "floor-upper",
        "parts": [
            {
                "type": "image",
                "image_id": "floor-1x1-exact",
                "x": 0,
                "y": 0
            },
            {
                "type": "component",
                "component_id": "floor-2x2-exact",
                "x": 2,
                "y": 3
            }
        ],
        "tags": [
            "example"
        ]
    }
    component_leaf = ComponentAsset(data_leaf, 'test_assetpack_name')
    assets = {"test_assetpack_name.i.floor-1x1-exact":
              FakeImageAsset('imageOne'),
              "test_assetpack_name.c.floor-2x2-exact":
              component_leaf
              }
    fake_asset_pack = FakeAssetPack(assets)
    component_branch = ComponentAsset(data_branch, 'test_assetpack_name')
    ill = component_branch.get_image_location_list(5, 7, fake_asset_pack)
    if len(ill) != 3:
        raise AssertionError()
    returned_image, offset_x, offset_y = ill[0]
    if not returned_image == 'imageOne':
        raise AssertionError()
    if not offset_x == 5:
        raise AssertionError()
    if not offset_y == 7:
        raise AssertionError()
    returned_image, offset_x, offset_y = ill[1]
    if not returned_image == 'imageOne':
        raise AssertionError()
    if not offset_x == 7:
        raise AssertionError(offset_x)
    if not offset_y == 10:
        raise AssertionError(offset_y)
    returned_image, offset_x, offset_y = ill[2]
    if not returned_image == 'imageOne':
        raise AssertionError()
    if not offset_x == 9:
        raise AssertionError(offset_x)
    if not offset_y == 13:
        raise AssertionError(offset_y)
