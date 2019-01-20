#!/usr/bin/env python3
# import profile
import os
import sys
from itertools import chain
from typing import *

from LsLinelist import DirLines, FileLines


class FSystem:

    def __init__(self):
        self._file_lines = FileLines()
        self._dir_lines = DirLines()

    def __repr__(self):
        return '{!r} \n{!r}'.format(self._file_lines, self._dir_lines)

    def __str__(self):
        return '\n'.join(
            chain.from_iterable(
                [self._dir_lines.get_lines(),
                 self._file_lines.get_lines()]))

    def add(self, e, stats):
        if e.is_file():
            self._file_lines.add(e, stats)
        else:
            self._dir_lines.add(e, stats)

    def complete(self):
        list_compress = []
        for fline in self._file_lines.get_raw_lines():
            if fline.is_backup:
                if self._file_lines.mark_backup_line(fline):
                    list_compress.append(0)
                else:
                    list_compress.append(1)
            else:
                list_compress.append(1)
        self._file_lines.delete_lines(list_compress)
        self._file_lines.complete()
        self._dir_lines.complete()


def _get_entries(_path: str):
    entries = FSystem()
    with os.scandir(_path) as osscandir:
        for e in osscandir:
            entries.add(e, e.stat())
    entries.complete()
    return entries


def main():
    if len(sys.argv) > 1:
        _path = sys.argv[1]
    else:
        _path = '.'
    print(_get_entries(_path))


if __name__ == "__main__":
    # profile.run("pmain()")
    main()
