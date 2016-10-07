import os
import shutil
from map_tools import merge_tiles
from nose.tools import eq_, ok_

test_data = {
		"16/38876/31140.png" : [ "tests/data/src2" ],
		"16/38877/31140.png" : [ "tests/data/src2" ],
		"16/38877/31141.png" : [ "tests/data/src1" ],
		"16/38878/31141.png" : [ "tests/data/src1" ],
		"16/38878/31142.png" : [ "tests/data/src1" ],
		"16/38877/31142.png" : [ "tests/data/src1", "tests/data/src2" ]
}
expected_paths = [path for path in test_data ]
src =  [ "tests/data/src1", "tests/data/src2" ]
dest_dir = "tests/data/out"


"""
Tests the collect_files function
"""
def test_collect_files():
	src = ["tests/data/src1", "tests/data/src2"]
	result = merge_tiles.collect_files(src)
	actual_paths = [path for path in result ]
	eq_(len(expected_paths), len(actual_paths))

	for path in result:
		ok_(path in test_data, "missing path {}".format(path))
		eq_(len(test_data[path]), len(result[path]))
		for root in result[path]:
			ok_(root in test_data[path], 
				"missing root {} in path {}".format(root, path))

"""
Tests the merge_files function
"""
def test_merge():
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
	merge_tiles.merge(src, dest_dir)
	files = []
	for s, d, fs in os.walk(dest_dir):
		for f in fs:
			files.append(f)
	eq_(len(expected_paths), len(files))
