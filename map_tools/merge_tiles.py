from PIL import Image
import os
import shutil


def collect_files(src):
    """
    Walks a python directory structure for a collection of
    source sirectories and returns a list of files and whether
    to merge
    """
    file_list = dict()
    for root in src:
        for subdir, dirs, files in os.walk(root):
            for f in files:
                relpath = os.path.relpath(
                    os.path.join(subdir, f), root)
                if relpath in file_list:
                    file_list[relpath].append(root)
                else:
                    file_list[relpath] = [root]
    return file_list


def merge(src, dest):
    """
    Merge two directories merging images file if necessary
    """
    paths = collect_files(src)
    for f in paths:
        f_dir = os.path.join(dest, os.path.dirname(f))
        if not os.path.exists(f_dir):
            os.makedirs(f_dir)
        if len(paths[f]) == 1:
            src_file = os.path.join(paths[f][0], f)
            dest_file = os.path.join(dest, f)
            shutil.copyfile(src_file, dest_file)
            print "copied {} to {}".format(src_file, dest_file)
        else:
            src_file1 = os.path.join(paths[f][0], f)
            src_file2 = os.path.join(paths[f][1], f)
            background = Image.open(src_file1)
            foreground = Image.open(src_file2)
            background.paste(foreground, (0, 0), foreground)
            dest_file = os.path.join(dest, f)
            background.save(dest_file, "PNG")
            print "merged {} and {} to {}".format(src_file1, src_file2, dest_file)
