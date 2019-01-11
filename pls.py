#!/usr/bin/env python3
# import profile
import math
import os
import sys
import typing as T
from collections import namedtuple
from datetime import datetime as dt
from datetime import timedelta
from itertools import zip_longest

import tabulate as tb
from tabulate import tabulate

from FNums import FSize, FTime


class FSystem:

    def _split(test, data):
        o1, o2 = [], []
        for i in data:
            if test(i):
                o1.append(i)
            else:
                o2.append(i)
        return o1, o2

    def __init__(self, current_time):
        self.lines = []
        self._regular = []
        self._other = []
        self.current_time = current_time
        self.is_split = False

    def _generate_line(self, e, stats):
        pass

    def __repr__(self):
        return '<{!r}>{!r}'.format(self.current_time, self.lines)

    def __str__(self):
        if (self.is_split):
            return '\n'.join(
                map(lambda x: tabulate(self._sort(x)),
                    [self._other, self._regular]))
        return tabulate(self._sort(self.lines))

    def _test_dot(line):
        return line.name.startswith('.')

    def _test_backup(line):
        return line.name.endswith('~')

    def _test_underscore(line):
        return line.name.startswith('_')

    def _test(self):
        pass

    def add(self, e, stats):
        self.lines.append(self._generate_line(e, stats))

    def split_lines(self):
        self._regular, self._other = FSystem._split(self._test, self.lines)
        self.is_split = True

    @property
    def regular(self):
        return self._sort(self._regular)

    @property
    def other(self):
        return self._sort(self._other)


class FFiles(FSystem):

    def __init__(self, current_time):
        self.Nline = namedtuple('Nline',
                                ['name', 'size', 'modified', 'accessed'])
        return super().__init__(current_time)

    def _generate_line(self, e, stats):
        return self.Nline(
            name=e.name,
            size=FSize(stats.st_size),
            accessed=FTime(stats.st_atime, self.current_time),
            modified=FTime(stats.st_mtime, self.current_time),
        )

    def _test(self, line):
        return not any([FFiles._test_backup(line), FFiles._test_dot(line)])

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l.size, reverse=True)


class FDirs(FSystem):

    def __init__(self, current_time):
        self.Nline = namedtuple('Nline', [
            'name',
            'modified',
        ])
        return super().__init__(current_time)

    def _generate_line(self, e, stats):
        return self.Nline(
            name=e.name,
            modified=FTime(stats.st_mtime, self.current_time),
        )

    def _test(self, line):
        return not any([FDirs._test_dot(line), FDirs._test_underscore(line)])

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l.name)


def _tabulate_splitline(lines):
    return tabulate(lines, headers="keys", tablefmt='presto').splitlines()


def main():
    current_time = dt.now()
    files = FFiles(current_time)
    dirs = FDirs(current_time)
    arg = '.'
    if (len(sys.argv) > 1):
        arg = sys.argv[1]
    with os.scandir(arg) as osscandir:
        for e in osscandir:
            if (e.is_file()):
                files.add(e, e.stat())
            else:
                dirs.add(e, e.stat())
    files.split_lines()
    dirs.split_lines()
    print(
        tabulate(
            zip_longest(*map(_tabulate_splitline, [files.other, dirs.other]))))
    print(
        tabulate(
            zip_longest(
                *map(_tabulate_splitline, [files.regular, dirs.regular]))))


if __name__ == "__main__":
    # profile.run("main()")
    main()
