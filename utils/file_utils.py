import os
import fnmatch


def remove_extension(filepath):
    basename = os.path.basename(filepath)
    return os.path.splitext(basename)[0]


def num_bmp_files_in_directory(dirpath):
    return len(fnmatch.filter(os.listdir(dirpath), "*.bmp"))
