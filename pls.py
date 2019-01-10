#!/usr/bin/env python3
import os
from itertools import zip_longest
from tabulate import tabulate as tb
from datetime import datetime as dt
from datetime import timedelta
import math

import typing as T
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
        self.regular = []
        self.other = []
        self.current_time = current_time
        self.is_split = False

    def _generate_line(self, e, stats):
        pass

    def _sort(self, lines):
        pass

    def __repr__(self):
        return '<{!r}><{!r}>'.format(self.lines, self.current_time)

    def __str__(self):
        if (self.is_split):
            return '\n'.join(
                map(lambda x: tb(self._sort(x)), [self.other, self.regular]))
        return tb(self._sort(self.lines))

    def _test_dot(line):
        return line['name'].startswith('.')

    def _test_backup(line):
        return line['name'].endswith('~')

    def _test_underscore(line):
        return line['name'].startswith('_')

    def _test(self):
        pass

    def add(self, e, stats):
        self.lines.append(self._generate_line(e, stats))

    def split_lines(self):
        self.regular, self.other = FSystem._split(self._test, self.lines)
        self.is_split = True


class FFiles(FSystem):

    def _generate_line(self, e, stats):
        return {
            'name': e.name,
            'size': FSize(stats.st_size),
            'access': FTime(stats.st_atime, self.current_time),
            'modification': FTime(stats.st_mtime, self.current_time),
        }

    def _test(self, line):
        return not any([FFiles._test_backup(line), FFiles._test_dot(line)])

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l['size'], reverse=True)


class FDirs(FSystem):

    def _generate_line(self, e, stats):
        return {
            'name': e.name,
            'access': FTime(stats.st_atime, self.current_time),
        }

    def _test(self, line):
        return not any([FDirs._test_dot(line), FDirs._test_underscore(line)])

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l['name'])


def zip_file_dirs(line_dict1, line_dict2):
    if len(line_dict1) < len(line_dict2):
        line_dict1, line_dict2 = line_dict2, line_dict1
    output_lines = []
    for f, d in zip_longest(line_dict1, line_dict2, fillvalue={}):
        ol = list(f.values())
        ol.extend(list(d.values()))
        output_lines.append(ol)
    return output_lines


def main():
    current_time = dt.now()
    files = FFiles(current_time)
    dirs = FDirs(current_time)
    with os.scandir('.') as osscandir:
        for e in osscandir:
            if (e.is_file()):
                files.add(e, e.stat())
            else:
                dirs.add(e, e.stat())
    files.split_lines()
    dirs.split_lines()
    print(tb(zip_file_dirs(files.other, dirs.other), tablefmt='github'))
    print(tb(zip_file_dirs(files.regular, dirs.regular), tablefmt='github'))


if __name__ == "__main__":
    main()
