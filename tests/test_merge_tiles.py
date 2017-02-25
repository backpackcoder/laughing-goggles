import os
import shutil

from nose.tools import eq_, ok_

from map_tools import merge_tiles

test_data = {
    "16/38876/31140.png": ["tests/data/src2"],
    "16/38877/31140.png": ["tests/data/src2"],
    "16/38877/31141.png": ["tests/data/src1"],
    "16/38878/31141.png": ["tests/data/src1"],
    "16/38878/31142.png": ["tests/data/src1"],
    "16/38877/31142.png": ["tests/data/src1", "tests/data/src2"]
}
expected_paths = [path for path in test_data]
src = ["tests/data/src1", "tests/data/src2"]
dest_dir = "tests/data/out"


def test_collect_files():
    """
    Tests the collect_files function
    """
    result = merge_tiles.collect_files(src)
    actual_paths = [path2 for path2 in result]
    eq_(len(expected_paths), len(actual_paths))

    for path3 in result:
        ok_(path3 in test_data, "missing path {}".format(path3))
        eq_(len(test_data[path3]), len(result[path3]))
        for root in result[path3]:
            ok_(root in test_data[path3],
                "missing root {} in path {}".format(root, path3))


def test_merge():
    """
    Tests the merge_files function
    """
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    merge_tiles.merge(src, dest_dir)
    files = []
    for s, d, fs in os.walk(dest_dir):
        for f in fs:
            files.append(f)
    eq_(len(expected_paths), len(files))
