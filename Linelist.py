import typing as T
from datetime import datetime as dt
from itertools import compress

from Entry import FDirEntry, FFileEntry, FEntry


class FLines:

    def __init__(self, LineGenerator):
        self._lines: T.List[FFileEntry, FDirEntry] = []
        self._line_generator = LineGenerator
        self._current_time = dt.now()
        self._max_line = self._max_name = 12
        self._index = 0

    def add(self, e):
        line = self._line_generator(e, self._current_time)
        self._lines.append(line)

    def mark_backup_line(self, f_in_line):
        for index, fline in enumerate(self._lines, 0):
            if f_in_line.name[:-1] == fline.name:
                self._lines[index].append_backup_ending()
                return True
        return False

    def delete_lines(self, compression_index):
        self._lines = list(compress(self._lines, compression_index))

    def __str__(self) -> str:
        return '\n'.join(self.get_lines())

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, key: int):
        return self._lines[key]

    def _set_max_line(self):
        # self._max_line = max([len(i) for i in self._lines])
        self._max_name = max([len(i.name) for i in self._lines])
        self._max_line = self._max_name + 2 * 8 + 1

    def complete(self):
        if self._lines != []:
            self._set_max_line()
            self._lines = sorted(self._lines)

    def get_empty_line(self) -> str:
        return ' ' * (self._max_line + 2)

    def get_lines(self) -> T.List[str]:
        return [line.get_str(self._max_name) for line in self._lines]

    def get_raw_lines(self) -> T.List:
        return self._lines

    @property
    def max_name(self):
        return self._max_name

    @property
    def max_line(self):
        return self._max_line
