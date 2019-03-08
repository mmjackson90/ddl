"""
Tests Projections
"""

from ddl.projection import Projection


def test_get_grid_ratios():
    """ Tests a projection returns the correct ratios"""
    projection1 = Projection('topdown', 10, 10)
    projection2 = Projection('topdown', 20, 30)
    assert projection1.get_grid_ratios(projection2) == (2, 3)
