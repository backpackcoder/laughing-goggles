from PIL import Image
import os
import shutil

"""
Walks a python directory structure for a collection of
source sirectories and returns a list of files and whether
to merge
"""
def collect_files(src):
	file_list = dict()
	for root in src:
		for subdir, dirs, files in os.walk(root):
			for f in files:
				relpath = os.path.relpath(
					os.path.join(subdir, f), root)
				if relpath in file_list:
					file_list[relpath].append(root)
				else:
					file_list[relpath] = [ root ]				
	return file_list


"""
Merge two directories merging images file if necessary
"""
def merge(src, dest):
	paths = collect_files(src)
	for f in paths:
		f_dir =  os.path.join(dest, os.path.dirname(f))
		if not os.path.exists(f_dir):
			os.makedirs(f_dir)
		if len(paths[f]) == 1:
			srcFile = os.path.join(paths[f][0], f)
			destFile = os.path.join(dest, f)
			shutil.copyfile(srcFile, destFile)
			print "copied {} to {}".format(srcFile, destFile)
		else:
			srcFile1 = os.path.join(paths[f][0], f)
			srcFile2 = os.path.join(paths[f][1], f)
			background = Image.open(srcFile1)
			foreground = Image.open(srcFile2)
			background.paste(foreground, (0, 0), foreground)
			destFile = os.path.join(dest, f)
			background.save(destFile, "PNG")
			print "merged {} and {} to {}".format(srcFile1, srcFile2, destFile)
