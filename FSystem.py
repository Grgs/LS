
# import typing as T
from collections import namedtuple

from tabulate import tabulate

from FNums import FSize, FTime

class FSystem:

    @staticmethod
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
        if self.is_split:
            return '\n'.join(
                map(lambda x: tabulate(self._sort(x)),
                    [self._other, self._regular]))
        return tabulate(self._sort(self.lines))

    @staticmethod
    def _test_dot(line):
        return line.name.startswith('.')

    @staticmethod
    def _test_backup(line):
        return line.name.endswith('~')

    @staticmethod
    def _test_underscore(line):
        return line.name.startswith('_')

    def _test(self, line):
        pass

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l.size, reverse=True)

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
        super().__init__(current_time)
        self.nline = namedtuple('nline',
                                ['name', 'size', 'modified', 'accessed'])

    def _generate_line(self, e, stats):
        return self.nline(
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
        super().__init__(current_time)
        self.nline = namedtuple('nline', [
            'name',
            'modified',
        ])

    def _generate_line(self, e, stats):
        return self.nline(
            name=e.name,
            modified=FTime(stats.st_mtime, self.current_time),
        )

    def _test(self, line):
        return not any([FDirs._test_dot(line), FDirs._test_underscore(line)])

    def _sort(self, lines):
        return sorted(lines, key=lambda l: l.name)

