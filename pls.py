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
            map(str, [
                dirs.other,
                dirs.regular,
                files.other,
                files.regular,
            ])))

    # print('-' * 60)
    # print('\n'.join(map(str, [
    #     files.other,
    #     files.regular,
    # ])))

    # print('\n'.join(map(str, [
    #     dirs.other,
    #     dirs.regular,
    #     files.regular,
    # ])))

    # print('\n'.join(dirs.regular))

    # print(files)
    # for i in ['other', 'regular']:
    #     print(_zip_tabulate(files, dirs, i))


if __name__ == "__main__":
    # profile.run("main()")
    main()
