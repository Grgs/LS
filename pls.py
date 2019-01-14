#!/usr/bin/env python3
# import profile
import os
import sys
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


def main():
    files = FFiles('file')
    dirs = FDirs('dir')
    arg = '.'
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    with os.scandir(arg) as osscandir:
        for e in osscandir:
            if e.is_file():
                files.add(e, e.stat())
            else:
                dirs.add(e, e.stat())
    str_seperator = ('\n' + '-' * 60 + '\n')
    print(
        str_seperator.join(
            map(str, [
                dirs.other,
                dirs.regular,
                files.other,
                files.regular,
            ])))


if __name__ == "__main__":
    # profile.run("main()")
    main()
