from map_tools import shp_utils
from nose.tools import eq_
from os import getcwd

test_shp_file = 'data/shp_files/at_centerline/at_centerline.shp'


def test_find_start_line():
    """
    Tests the collect_files function
    """
    print getcwd()
    first_line = shp_utils.find_start_line(test_shp_file)
    eq_(first_line, 341)
