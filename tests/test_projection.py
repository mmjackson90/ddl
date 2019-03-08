"""
Tests Projections
"""

from ddl.projection import Projection, IsometricProjection, TopDownProjection


def test_get_grid_ratios():
    """ Tests a projection returns the correct ratios"""
    projection1 = Projection(10, 10)
    projection2 = Projection(20, 30)
    assert projection1.get_grid_ratios(projection2) == (2, 3)


def test_alter_grid_parameters():
    """ Tests a projection returns the correct ratios"""
    projection1 = Projection(10, 10)
    projection2 = Projection(20, 30)
    projection1.alter_grid_parameters(projection2)
    assert projection1.width == 20
    assert projection1.height == 30


def test_isometric_get_pixels():
    projection = IsometricProjection(16, 10)
    assert projection.get_location_in_pixels(0, 0) == (0, 0)
    assert projection.get_location_in_pixels(1, 0) == (-8, 5)
    assert projection.get_location_in_pixels(1, 1) == (0, 10)
    assert projection.get_location_in_pixels(1, -1) == (-16, 0)


def test_topdown_get_pixels():
    projection = TopDownProjection(16, 10)
    assert projection.get_location_in_pixels(0, 0) == (0, 0)
    assert projection.get_location_in_pixels(1, 0) == (16, 0)
    assert projection.get_location_in_pixels(1, 1) == (16, 10)
    assert projection.get_location_in_pixels(1, -1) == (16, -10)
