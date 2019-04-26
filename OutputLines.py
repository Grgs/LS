import os
from itertools import chain, zip_longest
from typing import *

from FileEntry import FDirEntry, FFileEntry
from FileLines import FLines


class OutputLines:

    def __init__(self):
        self._file_lines = FLines(FFileEntry)
        self._dir_lines = FLines(FDirEntry)
        self._finalized = False

    def __repr__(self):
        return '{!r} \n{!r}'.format(self._file_lines, self._dir_lines)

    def __str__(self):
        return '\n'.join(
            chain.from_iterable(
                [self._dir_lines.get_lines(),
                 self._file_lines.get_lines()]))

    def add(self, e):
        if e.is_file:
            self._file_lines.add(e)
        else:
            self._dir_lines.add(e)

    def _add_empty_start(self, line: str):
        empty = self._file_lines.get_empty_line()
        return empty + line[2:] if line.startswith('  ') else line

    def _finalize(self):
        self._file_lines.delete_tmps_from_list()
        self._file_lines.finalize()
        self._dir_lines.finalize()
        self._finalized = True

    def get_lines(self):
        if not self._finalized:
            self._finalize()
        line_output = list(
            zip_longest(
                self._file_lines.get_lines(),
                self._dir_lines.get_lines(),
                fillvalue=' '))
        text = list(map(self._add_empty_start, map(' | '.join, line_output)))
        return '\n'.join(text)
