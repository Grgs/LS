from datetime import datetime as dt
from typing import *

from FLines import FDirLine, FFileLine, FLineList


class FSystem:

    def __init__(self, line_type: str, current_time=dt.now()):
        self._regular = FLineList(self._sort)
        self._backup = FLineList(self._sort)
        self._other = FLineList(self._sort)
        self.current_time = current_time
        self.line_gen = FFileLine if line_type == 'file' else FDirLine

    def __repr__(self):
        return '<{!r}>{!r} \n{!r}'.format(self.current_time, self._regular,
                                          self._other)

    def __str__(self):
        return '\n'.join(map(str, [self._other, self._regular]))

    @staticmethod
    def _test_dot(line):
        return line.name.startswith('.')

    @staticmethod
    def _test_backup(line):
        return line.name.endswith('~')

    @staticmethod
    def _test_underscore(line):
        return line.name.startswith('_')

    @classmethod
    def _test(cls, line):
        pass

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.name, reverse=True)

    def add(self, e, stats):
        line = self.line_gen(e, stats, self.current_time)
        if self._test_backup(line):
            self._backup.add(line)
        elif self._test(line):
            self._regular.add(line)
        else:
            self._other.add(line)

    def complete(self):
        for i in [self._regular, self._other, self._backup]:
            i.complete()

    def output(self):
        return [self._backup, self._other, self._regular]

    @property
    def regular(self):
        return self._regular

    @property
    def backup(self):
        return self._backup

    @property
    def other(self):
        return self._other


class FFiles(FSystem):

    @classmethod
    def _test(cls, line):
        return not cls._test_dot(line)

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.size, reverse=True)


class FDirs(FSystem):

    @classmethod
    def _test(cls, line):
        return not any([cls._test_dot(line), cls._test_underscore(line)])

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.name)
