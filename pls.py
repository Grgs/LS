#!/usr/bin/env python3
# import profile
import os
import sys
from datetime import datetime as dt
from itertools import zip_longest

from tabulate import tabulate

from FSystem import FDirs, FFiles


def _tabulate_splitline(lines):
    return tabulate(lines, headers="keys", tablefmt='presto').splitlines()


def _zip_tabulate(files, dirs, part: str):
    return tabulate(
        zip_longest(*map(
            _tabulate_splitline,
            [getattr(files, part), getattr(dirs, part)])))


# class FLine:

#     def __init__(self, e, stats, current_time):
#         self._line = [
#             e.name,
#             FSize(stats.st_size),
#             FTime(stats.st_atime, current_time),
#             FTime(stats.st_mtime, current_time),
#         ]


def main():
    current_time = dt.now()
    files = FFiles(current_time)
    dirs = FDirs(current_time)
    arg = '.'
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    with os.scandir(arg) as osscandir:
        for e in osscandir:
            if e.is_file():
                files.add(e, e.stat())
            else:
                dirs.add(e, e.stat())
    files.split_lines()
    dirs.split_lines()

    for i in ['other', 'regular']:
        print(_zip_tabulate(files, dirs, i))


if __name__ == "__main__":
    # profile.run("main()")
    main()
