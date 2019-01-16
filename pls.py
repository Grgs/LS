#!/usr/bin/env python3
# import profile
import os
import sys
from itertools import zip_longest
from datetime import datetime as dt

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
    current_time = dt.now()
    files = FFiles('file', current_time)
    dirs = FDirs('dir', current_time)
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
            filter(lambda x: x != '',
                   map(str, [
                       dirs.backup,
                       files.backup,
                       dirs.other,
                       dirs.regular,
                       files.other,
                       files.regular,
                   ]))))


if __name__ == "__main__":
    # profile.run("main()")
    main()
